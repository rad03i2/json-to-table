# Security / الأمان

JSON to Table performs local conversion only: it makes no network requests, executes no input, and requires no credentials. HTML output escapes cell values, but consumers should still apply their normal Content Security Policy when embedding generated HTML.

Do not process untrusted, extremely large JSON without resource limits: parsing occurs in memory. Report security issues privately to the maintainer through an appropriate GitHub private reporting channel when available; do not publish secrets in issues.

تعمل الأداة محليًا فقط ولا تجري اتصالات شبكية ولا تنفذ محتوى الإدخال ولا تحتاج إلى بيانات اعتماد. يتم تهريب قيم الخلايا في مخرجات HTML، ومع ذلك يُنصح بتطبيق سياسة أمان المحتوى المعتادة عند تضمين HTML الناتج.

يتم تحليل JSON في الذاكرة، لذلك لا تعالج ملفات ضخمة وغير موثوقة دون حدود للموارد. لا تنشر الأسرار في Issues العامة.
