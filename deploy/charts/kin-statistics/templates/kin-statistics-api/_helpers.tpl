{{/*
Expand the name of the chart.
*/}}
{{- define "kin-statistics.name" -}}
{{- default "kin-statistics" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-statistics.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-statistics.labels" -}}
helm.sh/chart: {{ include "kin-statistics.chart" . }}
{{ include "kin-statistics.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-statistics.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-statistics.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
