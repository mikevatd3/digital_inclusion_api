from sqlalchemy import MetaData, Table, select


"""
Table: acp_claims_by_zipcode

         Column          |         Type          
-------------------------+-----------------------
 id                      | bigint                
 data_month              | date                  
 zipcode                 | character varying(20) 
 claimed_subscribers     | double precision      
 claimed_devices         | double precision      
 claimed_service_support | double precision      
 claimed_device_support  | double precision      
 total_claimed_support   | double precision      
 zipcode_id              | integer               
 city_id                 | integer               
 county_id               | integer               

"""


class InvalidFieldException(Exception):
    """
    This exception is raised when the field requested on the geography
    isn't valid.
    """
    def __init__(self, *args: object, bad_fields=set()) -> None:
        """
        The exception stores which fields didn't work to pass back to the user.
        """
        super().__init__(*args)
        self.bad_fields=bad_fields


class ARPASource:
    def __init__(self, engine) -> None:
        self.metadata = MetaData()
        self.engine = engine

        self.acp_claims_by_zipcode = Table("acp_claims_by_zipcode", self.metadata, autoload_with=engine)


class ZipCodes:
    def __init__(self, source: ARPASource) -> None:
        self.source = source
        self.available_fields = {
            "zipcode",
            "data_month",
            "claimed_subscribers",
            "claimed_devices",
            "claimed_service_support",
            "claimed_device_support",
            "total_claimed_support",
        }


    def get_detail(self, zipcode, db, fields: list[str] = list()):
        bad_fields = {field for field in fields if field not in self.available_fields}
        if bad_fields:
            raise InvalidFieldException(f"Some fields not available on this geographic level.", bad_fields=bad_fields)

        columns = [
            self.source.acp_claims_by_zipcode.c[field]
            for field in fields
        ]

        stmt = select(*columns).where(
            self.source.acp_claims_by_zipcode.c.zipcode == zipcode
        )

        return db.execute(stmt).fetchone() 


    def get_list(self, filters, db, fields: list[str] = list()):
        bad_fields = {field for field in fields if field not in self.available_fields}
        if bad_fields:
            raise InvalidFieldException(f"The following fields are not available at this geographic level {bad_fields}")

        columns = [
            self.source.acp_claims_by_zipcode.c[field]
            for field in fields
        ]

        stmt = select(*columns)

        return db.execute(stmt).fetchall() 




