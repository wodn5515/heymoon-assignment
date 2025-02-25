from pydantic import BaseModel, model_validator
from datetime import datetime
from apps.dashboards.validations.exceptions import DateRangeNotValid


class DateRangeEntity(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date > self.end_date:
            raise DateRangeNotValid
        return self
