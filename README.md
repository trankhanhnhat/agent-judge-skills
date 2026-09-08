# Universal Agent Judge

**Skill giúp AI chấm bài làm theo yêu cầu, với bằng chứng cho từng kết luận.**

Đưa cho agent **đề bài + tiêu chí chấm + bài làm**. Skill hướng dẫn agent tìm, đọc và kiểm chứng bằng chứng, rồi trả về **đạt / chưa đạt / chưa đủ điều kiện đánh giá**. Hỗ trợ code, bản sửa lỗi, notebook ML, lịch sử dùng công cụ và file bàn giao.

**Tiếng Việt** · [English](README.en.md)

[Cài đặt](#cai-dat) · [Dùng thử](#dung-thu) · [Kết quả](#ket-qua) · [Cấu trúc repo](#cau-truc-repo)

```text
Đề bài + Bài làm → Tìm bằng chứng → Chấm từng yêu cầu → Khóa kết luận
                                                         ↓
                                           Đối chiếu đáp án nếu có
```

Ví dụ: với patch sửa bug, skill kiểm tra bản fix có giải quyết issue và được gọi trong luồng liên quan không. Với bài yêu cầu nộp PDF, skill kiểm tra file PDF thực tế; chỉ có script xuất PDF chưa đủ chứng minh đã nộp file.

<a id="cai-dat"></a>
## Cài đặt

Cần Node.js/npm để dùng lệnh cài:

```bash
npx skills add Nhatdangdihoc/agent-judge-skills --skill universal-agent-judge
```

Nếu đã tải repository về máy, chạy tại thư mục gốc:

```bash
npx skills add . --skill universal-agent-judge
```

Skill gồm hướng dẫn Markdown cho agent, JSON Schema và helper Python tùy chọn. **Dùng hướng dẫn không bắt buộc cài Python**; helper kiểm tra/xuất hồ sơ cần Python 3.10+ và `jsonschema`.

<a id="dung-thu"></a>
## Dùng thử

Chuẩn bị bài làm trong `./submission` và tiêu chí trong `./rubric.md`, rồi gửi agent prompt sau. Thay đường dẫn bằng dữ liệu thực tế của bạn:

```text
Sử dụng universal-agent-judge để chấm bài làm trong ./submission
theo đề bài và tiêu chí ở ./rubric.md.

Với từng yêu cầu, tự tìm và đọc các file liên quan, kiểm tra đường gọi
nếu cần, rồi kết luận bằng evidence cụ thể: file, dòng hoặc artifact.
Không sửa bài làm. Không tự thêm tiêu chí hoặc trọng số.

Xuất bảng Requirement ID, Verdict, Evidence, Confidence
và canonical JSON judgment. Ghi rõ phần chưa thể kiểm chứng.
```

Nếu có đáp án chuẩn để đối chiếu, bổ sung:

```text
Giữ ./gold.json chưa mở cho đến khi hoàn tất và khóa pre-reference judgment
bằng SHA-256. Sau đó mới đọc gold để đối chiếu, ghi bất đồng trong hồ sơ riêng
và không thay đổi verdict đã khóa.
```

> [!IMPORTANT]
> Để chấm độc lập, hãy tách đáp án/gold khỏi nội dung agent được xem ban đầu. Dặn “không đọc gold” không thể xóa thông tin đã lộ trong context.

## Có thể chấm những gì?

| Loại bài làm | Nội dung kiểm tra chính |
| --- | --- |
| Repository / workspace | Bằng chứng thực hiện yêu cầu; chức năng có được tích hợp và đi tới từ luồng liên quan |
| Function / class | Hợp đồng API, giá trị trả về, trường hợp biên và tác dụng phụ |
| Patch sửa lỗi | Behavior issue yêu cầu, callers/callees, đường gọi thực tế và regression liên quan |
| Lịch sử dùng công cụ | Các bước và kết quả quan sát được có hỗ trợ câu trả lời cuối không |
| Notebook / ML | Đúng dataset, bằng chứng thực thi thí nghiệm, đánh giá và kết quả đã lưu |
| File bàn giao / artifact | File thực sự đã nộp, nội dung, định dạng và đường dẫn được yêu cầu |

Đây là **skill chấm một bài làm cụ thể theo yêu cầu rõ ràng**. Agent thực hiện việc kiểm tra; helper Python hỗ trợ quản lý hồ sơ. Khi chấm patch, đối tượng được chấm là bản fix có sẵn, không phải khả năng skill tự sửa bug.

<a id="ket-qua"></a>
## Kết quả nhận được

| Nhãn | Ý nghĩa |
| --- | --- |
| `SATISFIED` | Có đủ bằng chứng cho tất cả điều kiện bắt buộc của yêu cầu |
| `UNSATISFIED` | Có bằng chứng quyết định rằng ít nhất một điều kiện bắt buộc không đạt |
| `NOT_EVALUABLE` | Chưa đủ điều kiện đánh giá, và chưa có bằng chứng quyết định để kết luận không đạt |

Mỗi yêu cầu có evidence, confidence và giới hạn kiểm tra. Hồ sơ xuất thành **Markdown và canonical JSON**. Khi một yêu cầu không đánh giá được, schema giữ semantic decision là `null`; không ép thành điểm 0 hoặc `UNSATISFIED`.

**Chỉ tính điểm có trọng số khi rubric cung cấp chính sách chấm.** Điểm nội dung, phạt hành chính và đánh giá ưu tiên được tách riêng. Confidence không tự đổi verdict.

Xem [ví dụ hồ sơ chấm](skills/universal-agent-judge/references/output-example.md) và [quy ước đầu ra](skills/universal-agent-judge/references/output-contract.md).

## Quy trình chấm

1. **Phân loại đầu vào:** đề bài, rubric, bài làm và gold/reference.
2. **Khóa yêu cầu:** giữ nguyên nghĩa, tách điều kiện nhỏ khi cần và xác định bằng chứng phải có.
3. **Tìm và kiểm chứng:** Locate → Search → Read → Graph/reachability; cân nhắc runtime khi cần và đủ an toàn.
4. **Ra quyết định:** kết luận theo evidence; nếu nói thành phần không tồn tại, ghi phạm vi và các bước tìm kiếm để chứng minh sự thiếu vắng — *Absence Proof*.
5. **Khóa hồ sơ:** lưu canonical JSON và SHA-256 trước khi mở reference.
6. **Đối chiếu nếu được yêu cầu:** ghi agreement/disagreement riêng, giữ nguyên phán quyết trước reference.

Code tồn tại không chứng minh nó đã chạy; tên hàm hay lời khẳng định trong README không thay thế bằng chứng. Nếu không thể chạy hoặc không đọc được artifact cần thiết, hồ sơ phải nêu rõ giới hạn. Hash giúp phát hiện hồ sơ bị sửa, không phải cơ chế lưu trữ bất biến ở cấp hệ thống.

<a id="cau-truc-repo"></a>
## Cấu trúc repo — từng phần để làm gì?

```text
skills/universal-agent-judge/
├── SKILL.md                      Điểm vào: quy trình và nguyên tắc chấm
├── references/                   Hướng dẫn chi tiết, được đọc khi cần
├── schemas/judgment.schema.json   Cấu trúc chuẩn của hồ sơ JSON
├── scripts/judgment.py            Helper kiểm tra, trình bày và quản lý truy cập
└── requirements.txt              Thư viện Python cho helper tùy chọn
```

**`references/` là tài liệu hướng dẫn cho judge, không phải thư mục chứa đáp án gold của bài được chấm.** Agent đọc những hướng dẫn liên quan đến loại bài hiện tại.

| Nhóm tài liệu | Chức năng | Bắt đầu từ |
| --- | --- | --- |
| `mode-*.md` | Sáu hướng dẫn: workspace, function, patch, trajectory, notebook/ML, artifact | [Workspace](skills/universal-agent-judge/references/mode-workspace.md), [Patch](skills/universal-agent-judge/references/mode-patch.md) |
| `input-roles.md`, `benchmark-adapters.md` | Phân biệt đầu vào và ánh xạ dữ liệu benchmark vào đối tượng cần chấm | [Vai trò đầu vào](skills/universal-agent-judge/references/input-roles.md) |
| `safe-candidate-execution.md`, `runtime-verification.md`, `notebook-execution.md` | Điều kiện thực thi an toàn và ghi nhận kiểm chứng runtime/notebook | [Thực thi an toàn](skills/universal-agent-judge/references/safe-candidate-execution.md) |
| `provenance.md`, `dataset-provenance.md` | Nguồn gốc evidence, file và nhận diện dataset | [Provenance](skills/universal-agent-judge/references/provenance.md) |
| `rubric-scoring.md` | Điểm, trọng số và chính sách do rubric quy định | [Chính sách điểm](skills/universal-agent-judge/references/rubric-scoring.md) |
| `output-contract.md`, `output-example.md` | Cấu trúc hồ sơ và ví dụ đầu ra | [Ví dụ](skills/universal-agent-judge/references/output-example.md) |
| `disagreement-audit.md`, `post-reference-metrics.md` | Phân tích bất đồng và tính metrics sau khi khóa judgment | [Audit bất đồng](skills/universal-agent-judge/references/disagreement-audit.md) |
| `flags-full.md` | Ý nghĩa các cờ chẩn đoán và giới hạn | [Danh mục flags](skills/universal-agent-judge/references/flags-full.md) |

Đọc [SKILL.md](skills/universal-agent-judge/SKILL.md) để xem nguyên tắc đầy đủ. Tên skill, schema keys và verdict giữ bằng tiếng Anh để dùng nhất quán với công cụ.

## Kiểm tra và xuất hồ sơ JSON

Chạy tại thư mục gốc repository sau khi đã có `audit.json` do agent tạo:

```bash
python -m pip install -r skills/universal-agent-judge/requirements.txt
python skills/universal-agent-judge/scripts/judgment.py validate audit.json
python skills/universal-agent-judge/scripts/judgment.py render audit.json --detail concise
```

`validate` kiểm tra hồ sơ theo schema và các quy tắc nhất quán; `render` trình bày thành Markdown. Có ba mức chi tiết: `concise`, `standard`, `forensic`, kèm JSON đầy đủ. **Helper không tự chấm code và không xác nhận verdict đúng chỉ vì JSON hợp lệ.**
