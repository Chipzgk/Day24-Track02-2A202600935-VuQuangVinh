# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: **dpo@medviet.vn / Hotline: 1900xxxx**

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. Technical Solutions cho phần còn thiếu

### 1. Audit logging (Platform Team)
- **Giải pháp**: Xây dựng một middleware AuditLogMiddleware trong ứng dụng FastAPI để tự động ghi nhận lại toàn bộ lịch sử truy cập của người dùng. Các trường thông tin cần ghi nhận bao gồm: `user_id`, `action`, `resource_accessed`, `timestamp`, `ip_address`.
- **Lưu trữ tập trung**: Đẩy tất cả logs về một hệ thống quản lý log tập trung như **ELK Stack (Elasticsearch, Logstash, Kibana)** hoặc lưu trữ dưới dạng Immutable Storage trên Cloud (ví dụ AWS CloudTrail / S3) để đảm bảo logs không thể bị chỉnh sửa hay xóa bỏ trái phép, phục vụ cho quá trình truy vết (Audit).

### 2. Breach detection (Security Team)
- **Giải pháp**: Sử dụng **Prometheus** kết hợp **Grafana** để giám sát các luồng traffic bất thường. Thiết lập các Rule cảnh báo (Alert) khi có các hành vi khả nghi, ví dụ: "Một tài khoản tải lượng lớn dữ liệu trong một thời gian ngắn" hoặc "Có nhiều IP từ nước ngoài cố truy cập API".
- **Hệ thống cảnh báo**: Triển khai thêm các công cụ SIEM (Security Information and Event Management) kết hợp AI để rà soát hành vi bất thường, tự động chặn IP (Rate Limiting/WAF) và gửi tin nhắn cảnh báo khẩn cấp đến đội ngũ ứng cứu sự cố (Incident Response Team) qua Slack/Email ngay lập tức.
