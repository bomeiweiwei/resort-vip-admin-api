from sqlalchemy import text
from sqlalchemy.orm import Session


class VipPromptService:
    def __init__(self, db: Session):
        self.db = db

    def get_customer_prompt_data(self, customer_id: str):
        sql = text("""
            SELECT
                c.FullName AS full_name,
                sg.GenderName AS gender_name,

                DATEDIFF(YEAR, c.BirthDate, GETDATE())
                -
                CASE
                    WHEN DATEADD(
                        YEAR,
                        DATEDIFF(YEAR, c.BirthDate, GETDATE()),
                        c.BirthDate
                    ) > GETDATE()
                    THEN 1
                    ELSE 0
                END AS age,

                sc.CountryName AS country_name,

                DATEDIFF(DAY, bs.CheckInDate, bs.CheckOutDate) AS stay_days,

                rt.RoomTypeName AS room_type_name,

                bs.AdultCount + bs.ChildCount AS total_count,

                CASE
                    WHEN bs.HasParking = 1
                    THEN N'有'
                    ELSE N'無'
                END AS has_parking

            FROM CustomerVipAccount cva
                INNER JOIN Customer c
                    ON cva.CustomerId = c.CustomerId

                INNER JOIN SysGender sg
                    ON c.GenderId = sg.GenderId

                INNER JOIN SysCountry sc
                    ON c.CountryCode = sc.CountryCode

                INNER JOIN BookingStay bs
                    ON c.CustomerId = bs.CustomerId

                INNER JOIN Room r
                    ON bs.RoomId = r.RoomId

                INNER JOIN RoomType rt
                    ON r.RoomTypeId = rt.RoomTypeId

            WHERE
                c.CustomerId = :customer_id
        """)

        result = self.db.execute(
            sql,
            {
                "customer_id": customer_id
            }
        ).mappings().first()

        return result