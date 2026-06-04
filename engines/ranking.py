class BuffettRankingEngine:

    def __init__(self):

        self.results = []

    def add_stock(
        self,
        ticker,
        decision_score,
        decision_rating
    ):

        self.results.append({

            "ticker":
                ticker,
        
            "decision_score":
                decision_score,
        
            "decision_rating":
                decision_rating
        
        })

    def ranking(self):

        return sorted(

            self.results,

            key=lambda x:
                x[
                    "decision_score"
                ],

            reverse=True

        )
