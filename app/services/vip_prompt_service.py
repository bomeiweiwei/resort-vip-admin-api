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
                bs.CheckInDate AS check_in_date,

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
                sc.CountryCode AS country_code,

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

        if result is None:
            raise ValueError(
                f"Customer {customer_id} prompt data not found."
            )

        return dict(result)
    
    def get_customer_booking_stay_notes(self, customer_id: str):
        sql = text("""
            SELECT 
                bsn.NoteType,
                bsn.NoteContent
            FROM 
            BookingStayNote bsn
                INNER JOIN BookingStay bs on bsn.BookingStayId = bs.BookingStayId
                INNER JOIN Customer c on bs.CustomerId = c.CustomerId
            WHERE
            c.CustomerId = :customer_id
        """)

        result = self.db.execute(
            sql,
            {
                "customer_id": customer_id
            }
        ).mappings().all()

        return [dict(row) for row in result]