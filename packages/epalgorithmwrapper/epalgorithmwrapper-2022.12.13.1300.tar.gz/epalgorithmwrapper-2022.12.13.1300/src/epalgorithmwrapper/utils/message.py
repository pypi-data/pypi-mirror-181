from datetime import datetime, timezone

def get_message_formatter():
    return StandardMessageFormatter()

class StandardMessageFormatter:
    def get_message(self, sub_job_reference, status, description) -> str:
        now = datetime.now(timezone.utc).isoformat()

        return f"""
        {{
            \"message-type\":\"algorithm-response\",
            \"date-time\":\"{now}\",
            \"sub-job-reference\":\"{sub_job_reference}\",
            \"status\":\"{status}\",
            \"description\":\"{description}\"
        }}
        """.strip()