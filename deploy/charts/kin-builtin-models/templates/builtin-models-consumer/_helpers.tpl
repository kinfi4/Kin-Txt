{{/*
Expand the name of the chart.
*/}}
{{- define "kin-builtin-models.name" -}}
{{- default "kin-builtin-models" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-builtin-models.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-builtin-models.labels" -}}
helm.sh/chart: {{ include "kin-builtin-models.chart" . }}
{{ include "kin-builtin-models.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-builtin-models.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-builtin-models.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
