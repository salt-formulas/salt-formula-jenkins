{%- if job_template.get('enabled', true) %}
  {#- Matrix way, simulating behavior of Jenkins job builder, not fully
      supported at the moment #}
  {%- for param_name, params in job_template.get('param', {}).iteritems() %}
    {%- set replacer = client.replacer.open + param_name + client.replacer.close %}
    {%- for param in params %}
      {%- set job_name = job_template.name|replace(replacer, param) %}
      {%- set job = job_template.template|yaml|replace(replacer, param)|load_yaml %}
      {%- include "jenkins/client/_job.sls" %}
    {%- endfor %}
  {%- endfor %}

  {#- Simple list of jobs togenerate with multiple parameters to replace #}
  {%- for job_params in job_template.get('jobs', []) %}
    {%- set _job_name = [job_template.name] %}
    {%- set _job = [job_template.template] %}

    {%- for key, value in job_params.iteritems() %}
      {#- You may think WTF hack is this but we can't update variables in
          inner scope to replace all parameters. But we can abuse lists for
          this purpose }:-) #}
      {%- set replacer = client.replacer.open + key + client.replacer.close %}
      {%- do _job_name.append(_job_name|last|replace(replacer, value)) %}
      {%- do _job.append(_job|last|yaml|replace(replacer, value)|load_yaml) %}
    {%- endfor %}

    {%- set job_name = _job_name|last %}
    {%- set job = _job|last %}
    {%- include "jenkins/client/_job.sls" %}
  {%- endfor %}
{%- endif %}
