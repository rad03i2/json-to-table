# JSON to Table

A small, dependency-free Python toolkit that converts JSON records into clean **Markdown, CSV, HTML, or terminal tables**. It works as both a CLI and a Python library, supports nested-object flattening, Unicode, column selection/reordering, stdin pipelines, and safe HTML escaping.

## Why it exists

APIs and scripts often produce JSON while reports, documentation, spreadsheets, terminals, and static pages need tabular output. JSON to Table provides one predictable local conversion layer without a web service or runtime dependency.

## Features

- JSON object or array-of-objects input
- Markdown, RFC-style CSV, HTML, and aligned text output
- Optional nested-object flattening with configurable separator
- Lists preserved as compact JSON values
- Deterministic first-seen column order
- Column selection and reordering
- UTF-8/Arabic-friendly output
- stdin/stdout pipelines and file output
- HTML cell escaping for untrusted values
- Python API with no runtime dependencies
- Clear validation errors and exit code `2` on failure

## Preview

```console
$ json-to-table examples/people.json --flatten --columns id,name,location.city -f markdown
| id | name | location.city |
| --- | --- | --- |
| 1 | Radwan | Mosul |
| 2 | سارة | Baghdad |
```

For screenshots, capture the terminal command above; the project itself does not require a graphical UI.

## Requirements & installation

- Python 3.10+

```bash
git clone https://github.com/rad03i2/json-to-table.git
cd json-to-table
python -m pip install -e .
```

For development/testing:

```bash
python -m pip install pytest
pytest -q
```

## Usage

```bash
json-to-table data.json
json-to-table data.json -f csv -o table.csv
json-to-table data.json --flatten -f text
json-to-table data.json --flatten --separator _ --columns id,user_name
cat data.json | json-to-table - -f html > table.html
python -m json_to_table data.json -f markdown
```

`--columns` is a comma-separated list and also controls output order. Unknown columns are rejected rather than silently omitted.

### Python API

```python
from json_to_table import convert

records = [{"name": "Radwan", "meta": {"city": "Mosul"}}]
print(convert(records, "markdown", flatten_nested=True))
```

## Configuration

There are no environment variables, credentials, network services, or config files. Behavior is controlled entirely by CLI flags or function arguments.

## Project structure

```text
src/json_to_table/   core library, CLI, module entry point
tests/               core and CLI tests
examples/            sample JSON input
.github/workflows/   cross-platform CI
```

## Testing

CI installs the package on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13, compiles the source, runs pytest, and smoke-tests the installed CLI. Tests cover Unicode, missing fields, nested flattening, list serialization, column ordering, HTML escaping, Markdown escaping, invalid structures, invalid JSON, and file output.

## Security & privacy

Conversion is local. The program makes no network requests, executes no JSON content, and requires no secrets. HTML cell values are escaped. JSON is parsed fully in memory, so apply external resource limits when processing very large untrusted files. See [SECURITY.md](SECURITY.md).

## Limitations

- Top-level arrays must contain objects; scalar arrays are intentionally rejected.
- Nested lists are serialized into a cell rather than expanded into multiple rows.
- JSON is loaded in memory; this is not a streaming multi-gigabyte parser.
- Terminal alignment uses Python string length, so visual width can differ for some emoji/CJK characters.
- It converts values; it does not infer schemas or data types for downstream databases.

## Optional roadmap

Potential future additions include JSON Lines input and configurable list expansion. These are optional; the current core workflow is complete without them.

## Contributing & license

See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية — JSON إلى جدول

أداة Python صغيرة بلا اعتماديات تشغيل خارجية لتحويل سجلات JSON إلى جداول مرتبة بصيغ **Markdown وCSV وHTML والنص الطرفي**. تعمل كسطر أوامر وكمكتبة Python، وتدعم تسطيح الكائنات المتداخلة وUnicode واختيار الأعمدة وترتيبها والعمل عبر stdin، مع تهريب آمن لقيم HTML.

## لماذا هذا المشروع؟

تنتج الواجهات البرمجية والسكربتات بيانات JSON بكثرة، بينما تحتاج التقارير والتوثيق والجداول وصفحات الويب والطرفية إلى عرض جدولي. يوفر المشروع طبقة تحويل محلية واضحة ومتوقعة دون خدمة ويب أو اعتماديات تشغيل إضافية.

## الميزات

- قبول كائن JSON واحد أو مصفوفة من الكائنات
- إخراج Markdown وCSV وHTML وجدول نصي بمحاذاة واضحة
- تسطيح اختياري للكائنات المتداخلة مع فاصل قابل للتغيير
- الاحتفاظ بالقوائم داخل الخلية بصيغة JSON مضغوطة
- ترتيب ثابت للأعمدة حسب أول ظهور
- اختيار الأعمدة وإعادة ترتيبها
- دعم UTF-8 والعربية
- القراءة من stdin والكتابة إلى stdout أو ملف
- تهريب قيم HTML قبل إدراجها في الخلايا
- Python API بلا اعتماديات تشغيل خارجية
- رسائل تحقق واضحة ورمز خروج `2` عند الخطأ

## المعاينة

```console
json-to-table examples/people.json --flatten --columns id,name,location.city -f markdown
```

الناتج جدول يحوي `id` و`name` و`location.city`. ولإنشاء لقطة شاشة للمشروع يكفي تصوير هذا الاستخدام في الطرفية؛ لا توجد واجهة رسومية مطلوبة.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/json-to-table.git
cd json-to-table
python -m pip install -e .
```

للتطوير والاختبارات:

```bash
python -m pip install pytest
pytest -q
```

## الاستخدام

```bash
json-to-table data.json
json-to-table data.json -f csv -o table.csv
json-to-table data.json --flatten -f text
json-to-table data.json --flatten --separator _ --columns id,user_name
cat data.json | json-to-table - -f html > table.html
python -m json_to_table data.json -f markdown
```

الخيار `--columns` يستقبل أسماء مفصولة بفواصل ويحدد ترتيبها أيضًا. إذا طُلب عمود غير موجود فتعيد الأداة خطأ بدل تجاهله بصمت.

### الاستخدام من Python

```python
from json_to_table import convert

records = [{"name": "رضوان", "meta": {"city": "الموصل"}}]
print(convert(records, "markdown", flatten_nested=True))
```

## الإعداد

لا توجد متغيرات بيئة أو مفاتيح API أو خدمة شبكية أو ملف إعداد. جميع الخيارات تأتي من معاملات CLI أو الدوال البرمجية.

## بنية المشروع

```text
src/json_to_table/   المحرك وواجهة CLI ونقطة تشغيل الموديول
tests/               اختبارات المحرك وCLI
examples/            بيانات JSON للتجربة
.github/workflows/   اختبارات CI متعددة الأنظمة
```

## الاختبارات

يفحص CI المشروع على Ubuntu وWindows وmacOS باستخدام Python 3.10 و3.12 و3.13، ويجري compile للمصدر ثم pytest واختبارًا سريعًا للأمر المثبت. تشمل الاختبارات Unicode والقيم المفقودة والتسطيح والقوائم وترتيب الأعمدة وتهريب HTML وMarkdown والمدخلات غير الصحيحة وأخطاء JSON وحفظ الملفات.

## الأمان والخصوصية

كل التحويل محلي؛ لا توجد طلبات شبكة ولا يتم تنفيذ محتوى JSON ولا توجد أسرار مطلوبة. يتم تهريب قيم خلايا HTML. يُحمّل JSON كاملًا في الذاكرة، لذا استخدم حدود موارد خارجية للملفات الضخمة غير الموثوقة. راجع [SECURITY.md](SECURITY.md).

## القيود

- المصفوفة العليا يجب أن تتكون من كائنات؛ مصفوفات القيم المفردة مرفوضة عمدًا.
- القوائم المتداخلة توضع داخل خلية ولا تتحول إلى صفوف متعددة.
- ليست الأداة محلل streaming لملفات بحجم عدة غيغابايت.
- محاذاة الطرفية تعتمد طول السلسلة في Python وقد تختلف بصريًا لبعض رموز emoji/CJK.
- لا تستنتج مخططات قواعد البيانات أو أنواع الحقول لها.

## تطوير اختياري لاحق

يمكن مستقبلًا إضافة JSON Lines وخيارات لتوسيع القوائم. هذه إضافات اختيارية وليست ضرورية لاكتمال الوظيفة الحالية.

## المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص وفق [MIT](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
