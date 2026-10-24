from app.agents.correlation_agent import CorrelationAgent
from app.agents.scoring_agent import ScoringAgent
from app.agents.hypothesis_builder import HypothesisBuilder
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.evidence_engine import EvidenceEngine

from app.database.repositories.diagnosis_repository import (
    DiagnosisRepository
)

from app.database.repositories.audit_repository import (
    AuditRepository
)


class RCAEngine:

    def run(
        self,
        events
    ):

        correlation = CorrelationAgent()
        scoring = ScoringAgent()
        builder = HypothesisBuilder()
        recommender = RecommendationAgent()
        evidence_engine = EvidenceEngine()

        findings = correlation.correlate(
            events
        )

        results = []

        for finding in findings:

            confidence = scoring.score(
                finding,
                len(events)
            )

            evidence = evidence_engine.collect(
                finding,
                events
            )

            hypothesis = builder.build(
                finding,
                confidence
            )

            hypothesis[
                "recommendation"
            ] = recommender.recommend(
                finding
            )

            hypothesis[
                "evidence"
            ] = evidence

            results.append(
                hypothesis
            )

        return results

    def persist_results(
        self,
        incident_id,
        results
    ):

        repo = DiagnosisRepository()
        audit = AuditRepository()

        try:

            for result in results:

                repo.create_analysis(
                    incident_id=incident_id,
                    root_cause=result["root_cause"],
                    confidence=result["confidence"],
                    recommendation=result["recommendation"]
                )

                audit.log(
                    action="RCA_ANALYSIS_CREATED",
                    entity_type="analysis",
                    entity_id=incident_id,
                    details=result["root_cause"]
                )

        except Exception as ex:

            try:
                repo.conn.rollback()
            except Exception:
                pass

            audit.log(
                action="RCA_ERROR",
                entity_type="analysis",
                entity_id=incident_id,
                details=str(ex)
            )

            raise

        finally:

            audit.close()
            repo.close()

    def run_and_save(
        self,
        incident_id,
        events
    ):

        results = self.run(
            events
        )

        self.persist_results(
            incident_id,
            results
        )

        return results

    def run_from_incident(
        self,
        incident_id
    ):

        repo = DiagnosisRepository()
        audit = AuditRepository()

        try:

            events = repo.get_events_by_incident(
                incident_id
            )

            if not events:

                audit.log(
                    action="RCA_NO_EVENTS",
                    entity_type="incident",
                    entity_id=incident_id,
                    details="No events found"
                )

                return []

            event_names = []

            for event in events:

                if (
                    isinstance(event, dict)
                    and "source" in event
                ):

                    event_names.append(
                        event["source"]
                    )

            results = self.run(
                event_names
            )

            self.persist_results(
                incident_id,
                results
            )

            audit.log(
                action="RCA_EXECUTED",
                entity_type="incident",
                entity_id=incident_id,
                details=f"Hypotheses generated: {len(results)}"
            )

            return results

        except Exception as ex:

            audit.log(
                action="RCA_ERROR",
                entity_type="incident",
                entity_id=incident_id,
                details=str(ex)
            )

            raise

        finally:

            audit.close()
            repo.close()