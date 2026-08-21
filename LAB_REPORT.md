# Báo Cáo Lab MLOps - Điểm Công Thành

## Kết quả thực nghiệm

Các thí nghiệm được theo dõi bằng MLflow trên cùng tập đánh giá 500 mẫu. Ba cấu hình tiêu biểu trên 2.998 mẫu huấn luyện:

| Thuật toán | Siêu tham số chính | Accuracy | F1-score |
|---|---|---:|---:|
| Random Forest | 100 cây, depth 5, split 2 | 0.564 | 0.5534 |
| Random Forest | 500 cây, depth không giới hạn, split 2 | 0.676 | 0.6748 |
| Extra Trees | 800 cây, depth không giới hạn, split 2 | 0.688 | 0.6859 |

Sau khi bổ sung `train_phase2`, tập huấn luyện tăng từ 2.998 lên 5.996 mẫu. Extra Trees với 100 cây, depth không giới hạn và `min_samples_split=2` đạt accuracy `0.7660`, F1-score `0.7654`. Đây là cấu hình được chọn vì đồng hạng accuracy cao nhất nhưng huấn luyện nhanh hơn các cấu hình 150 và 800 cây. So với Random Forest tốt nhất trên cùng dữ liệu (`accuracy=0.7460`), Extra Trees tăng 2 điểm phần trăm.

## Pipeline và bonus

Pipeline GitHub Actions gồm Unit Test, Train, Eval và Deploy. DVC tải dữ liệu từ S3; eval gate chỉ cho phép accuracy từ `0.70`; model đạt chuẩn được upload và service FastAPI trên EC2 được restart. Endpoint `/health` trả `{"status":"ok"}` và `/predict` trả `{"prediction":0,"label":"thap"}` cho mẫu kiểm tra.

Pipeline tạo `metrics.json` và `report.txt` gồm confusion matrix, precision và recall từng lớp. Phân phối nhãn được ghi vào metrics và cảnh báo nếu lớp nào dưới 10%. Trước khi promotion, accuracy mới được so với `models/latest/metrics.json`; model kém hơn sẽ không ghi đè model đang chạy. Workflow hỗ trợ MLflow từ xa qua ba GitHub Secrets `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME` và `MLFLOW_TRACKING_PASSWORD`.

## Khó khăn và cách giải quyết

Credential AWS ban đầu sai định dạng JSON làm job Train lỗi; đã chuẩn hóa secret và xuất đúng biến môi trường cho DVC/boto3. Tập 2.998 mẫu chỉ đạt tối đa 0.688 với các mô hình đã thử, trong khi sau khi bổ sung dữ liệu accuracy tăng lên 0.766 và vượt gate. Repo là fork nên GitHub chỉ chạy `workflow_dispatch` dù workflow đang active; cần bật workflow của fork trong giao diện Actions trước khi chụp bằng chứng push-triggered của Bước 3.
