from prowler.lib.check.models import Check, Check_Report
from prowler.providers.azure.services.defender.defender_client import defender_client


class defender_ensure_defender_for_os_relational_databases_is_on(Check):
    def execute(self) -> Check_Report:
        findings = []
        for subscription, pricings in defender_client.pricings.items():
            report = Check_Report(self.metadata())
            report.region = defender_client.region
            report.status = "PASS"
            report.resource_id = "Defender plan Open-Source Relational Databases"
            report.status_extended = f"Defender plan Defender for Open-Source Relational Databases from subscription {subscription} is set to ON (pricing tier standard)"
            if pricings["OpenSourceRelationalDatabases"].pricing_tier != "Standard":
                report.status = "FAIL"
                report.status_extended = f"Defender plan Defender for Open-Source Relational Databases from subscription {subscription}  is set to OFF (pricing tier not standard)"

            findings.append(report)
        return findings
