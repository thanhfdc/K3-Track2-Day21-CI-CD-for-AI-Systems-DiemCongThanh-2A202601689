# Bộ ảnh bằng chứng nộp bài

Các ảnh dưới đây được chụp trực tiếp từ GitHub, DagsHub/MLflow, AWS và API EC2.
Không ảnh nào hiển thị secret, access token, access key hoặc SSH private key.

## Ảnh bắt buộc

1. `11-local-mlflow-runs.png`: ba run MLflow với thuật toán, params, accuracy và F1 khác nhau.
2. `12-local-mlflow-compare.png`: biểu đồ Compare của ba run MLflow.
3. `02-github-step2-success.png`: run Bước 2, đủ Unit Test, Train, Eval và Deploy màu xanh.
4. `03-github-train-accuracy.png`: log Train có phân phối ba lớp, accuracy `0.7660` và F1 `0.7654`.
5. `05-github-artifact-metrics.png`: artifact `metrics` của GitHub Actions.
6. `13-dagshub-report-confusion-matrix.png`: `report.txt` có confusion matrix, precision, recall và F1 từng lớp.
7. `01-github-push-success.png`: run continuous training được kích hoạt bằng event `push`, commit `055dee9`.
8. `04-github-model-comparison.png`: candidate/deployed đều `0.7660` và `Promotion approved`.
9. `15-ec2-api-health-predict-live.png`: kiểm chứng live `/health` và `/predict`, cả hai HTTP 200.
10. `09-s3-dvc-files-md5.png`: dữ liệu DVC trong S3 tại `dvc/files/md5/`.
11. `10-s3-models-latest.png`: `model.pkl`, `metrics.json`, `report.txt` tại `models/latest/`.

## Ảnh bonus và bổ sung

- `06-dagshub-runs-list.png`: experiment `wine-quality-ci` và run CI `manual-5`.
- `07-dagshub-run-metrics.png`: metrics của run `manual-5` trên DagsHub.
- `08-dagshub-run-artifacts.png`: artifact model và `report.txt` của run DagsHub.
- `14-github-deploy-health-check.png`: log Deploy trả `{"status":"ok"}` và `Health check passed`.

Khi hệ thống nộp giới hạn đúng 10 ảnh, có thể gộp ảnh 5 và 6 thành một mục bằng chứng artifact,
đồng thời ưu tiên giữ đủ các ảnh 1, 2, 3, 4, 7, 8, 9, 10 và 11.

Artifact gốc của run push đã được tải vào `github-artifact-metrics/`, gồm
`metrics.json` và `report.txt`; nộp kèm thư mục này nếu cổng nộp bài cho phép.
