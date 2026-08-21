# Checklist Ảnh Và Bằng Chứng Nộp Bài

Chụp ảnh toàn màn hình, giữ thanh địa chỉ hoặc terminal prompt trong ảnh. Không chụp hay mở giá trị của GitHub Secrets, AWS access key hoặc SSH private key.

## 1. MLflow - Bước 1 và Bonus 2

1. Tại thư mục repo, chạy:

   ```powershell
   .\.venv\Scripts\mlflow.exe ui --backend-store-uri sqlite:///mlflow.db --port 5000
   ```

2. Mở `http://127.0.0.1:5000`, chọn experiment `Default`, sắp xếp `accuracy` giảm dần.
3. Ảnh 1: danh sách ít nhất ba run có `n_estimators`, `max_depth`, `accuracy`, `f1_score` khác nhau.
4. Ảnh 2: chọn một run Random Forest và một run Extra Trees, bấm **Compare**; giữ bảng params và metrics trong cùng ảnh.

## 2. GitHub Actions - Bước 2

1. Mở run xanh: `https://github.com/thanhfdc/K3-Track2-Day21-CI-CD-for-AI-Systems-DiemCongThanh-2A202601689/actions/runs/32473557644`.
2. Ảnh 3: trang summary hiển thị đủ bốn job xanh: Unit Test, Train, Eval, Deploy.
3. Mở job Train.
4. Ảnh 4: log `Accuracy: 0.7660`, ba tỷ lệ class và `Promotion approved`.
5. Ảnh 5: phần Artifacts ở cuối summary có artifact `metrics`; tải xuống và mở `report.txt` để hiện confusion matrix cùng precision/recall.

## 3. Continuous training - Bước 3

Repo fork hiện cần bật push workflow trong UI:

1. Vào **Actions → MLOps Pipeline**. Nếu có nút **Enable workflow** hoặc banner **I understand my workflows, go ahead and enable them**, bấm nút đó.
2. Vào **Settings → Actions → General**, chọn **Allow all actions and reusable workflows**, bấm **Save**.
3. Tăng trường `meta.version` trong `data/train_phase1.csv.dvc`, rồi chạy:

   ```powershell
   git add data/train_phase1.csv.dvc
   git commit -m "data: trigger continuous training with 5996 samples"
   git push origin main
   ```

4. Ảnh 6: run mới phải hiện đúng commit message trên và event `push`, không chọn run có event `workflow_dispatch`.
5. Ảnh 7: mở run đó, chụp đủ bốn job xanh. Trong log Train phải có `Model comparison: candidate=0.7660, deployed=0.7660` và `Promotion approved`.

## 4. API trên EC2

Chạy trong PowerShell:

```powershell
$VM_IP = "3.239.224.48"
curl.exe "http://$VM_IP`:8000/health"
curl.exe -X POST "http://$VM_IP`:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{"features":[7.4,0.70,0.00,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,0]}'
```

Ảnh 8 phải thấy cả `{"status":"ok"}` và `{"prediction":0,"label":"thap"}`.

## 5. S3 và bonus

1. Mở AWS Console → S3 → bucket `mlops-lab-138420161153-us-east-1`.
2. Ảnh 9: prefix `dvc/files/md5/` có các object dữ liệu.
3. Ảnh 10: `models/latest/` có `model.pkl`, `metrics.json`, `report.txt`.
4. Bonus DagsHub:
   - Đăng nhập `https://dagshub.com` bằng GitHub và import repo này.
   - Trong repo DagsHub, mở **Remote → Experiments** để lấy MLflow tracking URL và access token.
   - Trong GitHub **Settings → Secrets and variables → Actions**, tạo:
     - `MLFLOW_TRACKING_URI`: `https://dagshub.com/<DAGSHUB_USER>/<DAGSHUB_REPO>.mlflow`
     - `MLFLOW_TRACKING_USERNAME`: tên tài khoản DagsHub.
     - `MLFLOW_TRACKING_PASSWORD`: DagsHub access token, không phải mật khẩu đăng nhập.
   - Chạy lại pipeline. Ảnh 11 chụp DagsHub MLflow với experiment `wine-quality-ci`, params và metrics của run CI.

## 6. File nộp

- URL repo public.
- 10 ảnh bắt buộc ở trên; thêm ảnh DagsHub nếu lấy Bonus 1.
- `LAB_REPORT.md`, giữ nội dung không quá một trang A4 khi xuất PDF.
- Artifact `metrics` tải từ run Bước 3.
