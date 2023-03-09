{% include "jinja_template/license_header.md.j2" %}
# 🔐 Security Policy

> Do not open issues that might have security implications!
> It is critical that security related issues are reported privately so we have
> time to address them before they become public knowledge.

Vulnerabilities can be reported by emailing core members:

- {{author}} [{{email}}](mailto:{{email}})
{% if ci == "github" %}
Or using [GitHub draft security advisory](https://github.com/{{github_user}}/{{project_slug}}/security/advisories/new).
{% elif ci == "gitlab" %}
{% else %}
{% endif -%}
Be sure to include as much detail as necessary in your report. As with
reporting normal issues, a minimal reproducible example will help the
maintainers address the issue faster. If you are able, you may also include a
fix for the issue generated with git format-patch.
