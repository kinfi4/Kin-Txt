{{/*
Expand the name of the chart.
*/}}
{{- define "kin-api-gateway.name" -}}
{{- default "kin-api-gateway" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-api-gateway.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-api-gateway.labels" -}}
helm.sh/chart: {{ include "kin-api-gateway.chart" . }}
{{ include "kin-api-gateway.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-api-gateway.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-api-gateway.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
