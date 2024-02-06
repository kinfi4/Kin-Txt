{{/*
Expand the name of the chart.
*/}}
{{- define "kin-generic-models.name" -}}
{{- default "kin-generic-models" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-generic-models.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-generic-models.labels" -}}
helm.sh/chart: {{ include "kin-generic-models.chart" . }}
{{ include "kin-generic-models.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-generic-models.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-generic-models.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
