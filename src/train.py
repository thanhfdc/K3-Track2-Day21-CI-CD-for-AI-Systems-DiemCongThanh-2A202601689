import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

EVAL_THRESHOLD = 0.70
LABELS = [0, 1, 2]
LABEL_NAMES = ["thap", "trung_binh", "cao"]


def build_model(params: dict):
    model_params = params.copy()
    model_type = model_params.pop("model_type", "random_forest")
    model_params.setdefault("random_state", 42)

    if model_type == "random_forest":
        return RandomForestClassifier(**model_params)
    if model_type == "extra_trees":
        return ExtraTreesClassifier(**model_params)

    raise ValueError(f"Unsupported model_type: {model_type}")


def get_label_distribution(labels: pd.Series) -> dict[str, float]:
    """Return stable class ratios, including classes absent from the dataset."""
    ratios = labels.value_counts(normalize=True).reindex(LABELS, fill_value=0.0)
    return {str(label): float(ratios[label]) for label in LABELS}


def write_performance_report(y_true, predictions, path: str) -> None:
    """Write the text report uploaded by CI after every training run."""
    matrix = confusion_matrix(y_true, predictions, labels=LABELS)
    details = classification_report(
        y_true,
        predictions,
        labels=LABELS,
        target_names=LABEL_NAMES,
        digits=4,
        zero_division=0,
    )
    report = (
        "CONFUSION MATRIX (rows=true, columns=predicted)\n"
        "labels: 0=thap, 1=trung_binh, 2=cao\n"
        f"{matrix}\n\n"
        "PRECISION / RECALL / F1 BY CLASS\n"
        f"{details}"
    )
    with open(path, "w", encoding="utf-8") as report_file:
        report_file.write(report)


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho RandomForestClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia.

    Tra ve:
        accuracy (float): do chinh xac tren tap danh gia.
    """

    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI") or "sqlite:///mlflow.db"
    )
    experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME")
    if experiment_name:
        mlflow.set_experiment(experiment_name)

    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    label_distribution = get_label_distribution(y_train)
    print("Train label distribution:")
    for label, ratio in label_distribution.items():
        print(f"  class {label}: {ratio:.2%}")
        if ratio < 0.10:
            print(
                f"WARNING: class {label} is only {ratio:.2%} of training data "
                "(< 10%)."
            )

    with mlflow.start_run(run_name=os.getenv("MLFLOW_RUN_NAME")):
        mlflow.log_params(params)

        model = build_model(params)
        model.fit(X_train, y_train)

        preds = model.predict(X_eval)
        acc = accuracy_score(y_eval, preds)
        f1 = f1_score(y_eval, preds, average="weighted")
        precision, recall, _, _ = precision_recall_fscore_support(
            y_eval, preds, labels=LABELS, zero_division=0
        )

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        for index, label in enumerate(LABELS):
            mlflow.log_metric(f"precision_class_{label}", float(precision[index]))
            mlflow.log_metric(f"recall_class_{label}", float(recall[index]))
        mlflow.sklearn.log_model(model, "model")

        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        os.makedirs("outputs", exist_ok=True)
        with open("outputs/metrics.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "accuracy": float(acc),
                    "f1_score": float(f1),
                    "label_distribution": label_distribution,
                },
                f,
                indent=2,
            )

        write_performance_report(y_eval, preds, "outputs/report.txt")
        mlflow.log_artifact("outputs/report.txt")

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    return float(acc)


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
