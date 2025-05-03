from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Marker(Base):
    __tablename__ = "markers"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    comment = Column(String)
    photos = relationship("Photo", back_populates="marker", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="marker", cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    marker_id = Column(Integer, ForeignKey("markers.id"))
    marker = relationship("Marker", back_populates="photos")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    marker_id = Column(Integer, ForeignKey("markers.id"), nullable=False)
    marker = relationship("Marker", back_populates="comments")
