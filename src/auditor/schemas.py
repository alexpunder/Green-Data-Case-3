from dataclasses import dataclass


@dataclass
class Vulnerability:
    """Найденная уязвимость."""

    vuln_class: str
    risk_score: float
    description: str
    recommendation: str

    @property
    def to_dict(self):
        return {
            "vuln_class": self.vuln_class,
            "risk_score": self.risk_score,
            "description": self.description,
            "recommendation": self.recommendation,
        }


@dataclass
class AuditResult:
    """Результат проверки SQL."""

    approved: bool
    feedback: str
    vulnerabilities: list[Vulnerability]
    overall_risk_score: float
    summary: str
    tokens_used: int

    @property
    def to_dict(self):
        return {
            "approved": self.approved,
            "feedback": self.feedback,
            "vulnerabilities": [
                vulnerability.to_dict for vulnerability in self.vulnerabilities
            ],
            "overall_risk_score": self.overall_risk_score,
            "summary": self.summary,
            "tokens_used": self.tokens_used,
        }
