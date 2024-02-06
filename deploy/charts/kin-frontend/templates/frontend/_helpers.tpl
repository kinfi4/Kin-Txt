{{/*
Expand the name of the chart.
*/}}
{{- define "kin-frontend.name" -}}
{{- default "kin-frontend" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-frontend.labels" -}}
helm.sh/chart: {{ include "kin-frontend.chart" . }}
{{ include "kin-frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
