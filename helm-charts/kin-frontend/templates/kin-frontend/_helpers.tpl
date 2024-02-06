{{/*
Expand the name of the chart.
*/}}
{{- define "kin-model-types.name" -}}
{{- default "kin-model-types" }}
{{- end }}


{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kin-model-types.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kin-model-types.labels" -}}
helm.sh/chart: {{ include "kin-model-types.chart" . }}
{{ include "kin-model-types.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kin-model-types.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kin-model-types.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
