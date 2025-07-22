from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Provider(Base):
    __tablename__ = "providers"
    
    provider_id = Column(String, primary_key=True)  # Rndrng_Prvdr_CCN
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False, index=True)  # Index for radius search
    
    # Relationships
    procedures = relationship("Procedure", back_populates="provider")
    ratings = relationship("Rating", back_populates="provider", uselist=False)

class Procedure(Base):
    __tablename__ = "procedures"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(String, ForeignKey("providers.provider_id"))
    drg_code = Column(String, nullable=False, index=True)
    drg_description = Column(String, nullable=False)
    total_discharges = Column(Integer)
    avg_covered_charges = Column(Float)
    avg_total_payments = Column(Float)
    avg_medicare_payments = Column(Float)
    
    # Relationship
    provider = relationship("Provider", back_populates="procedures")
    
    # Index for DRG searches
    __table_args__ = (
        Index('idx_drg_search', 'drg_code', 'drg_description'),
    )

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(String, ForeignKey("providers.provider_id"), unique=True)
    rating = Column(Integer, nullable=False)  # 1-10
    
    # Relationship
    provider = relationship("Provider", back_populates="ratings")