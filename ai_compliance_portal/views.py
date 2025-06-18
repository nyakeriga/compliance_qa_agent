from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>✅ AI Compliance Portal</h1>
        <p>Welcome to your smart AI system. Use:</p>
        <ul>
            <li><a href="/admin/">/admin/</a> – Django Admin</li>
            <li><a href="/agent1/">/agent1/</a> – Compliance QA Agent</li>
            <li><a href="/agent2/">/agent2/</a> – News Intelligence Agent</li>
        </ul>
    """)

