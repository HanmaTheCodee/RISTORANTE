from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    CheckConstraint,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .database import Base


# ==================================================
# UTENTE
# ==================================================

class Utente(Base):
    __tablename__ = "utente"

    idUtente: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    cognome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    citta: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    regione: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    cap: Mapped[str] = mapped_column(
        String(25),
        nullable=False
    )

    # 1:1 con Account
    account: Mapped["Account | None"] = relationship(
        back_populates="utente",
        cascade="all, delete-orphan"
    
    )

    # 1:N con Ordine
    ordini: Mapped[list["Ordine"]] = relationship(
        back_populates="utente"
    )


# ==================================================
# ACCOUNT
# ==================================================

class Account(Base):
    __tablename__ = "account"

    idAccount: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    dataCreazione: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    passHash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ruolo: Mapped[str] = mapped_column(
        String(30),
        server_default="cliente",
        nullable=False
    )

    idUtente: Mapped[int] = mapped_column(
        ForeignKey("utente.idUtente"),
        unique=True,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "ruolo IN ('cliente', 'amministratore')",
            name="ck_account_ruolo"
        ),
    )

    utente: Mapped["Utente"] = relationship(
        back_populates="account"
    )


# ==================================================
# CUCINA
# ==================================================

class Cucina(Base):
    __tablename__ = "cucina"

    idCucina: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    numAddetti: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "numAddetti >= 0",
            name="ck_cucina_num_addetti"
        ),
    )

    ordini: Mapped[list["Ordine"]] = relationship(
        back_populates="cucina"
    
    )


# ==================================================
# RIDER
# ==================================================

class Rider(Base):
    __tablename__ = "rider"

    idRider: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    cognome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    ordini: Mapped[list["Ordine"]] = relationship(
        back_populates="rider"
    )


# ==================================================
# PAGAMENTO
# ==================================================

class Pagamento(Base):
    __tablename__ = "pagamento"

    idPagamento: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    modalitaPag: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    dataPag: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    statoPag: Mapped[str] = mapped_column(
        String(30),
        server_default="in_attesa",
        nullable=False
    )

    importoPag: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "importoPag >= 0",
            name="ck_pagamento_importo"
        ),
    )

    ordine: Mapped["Ordine | None"] = relationship(
        back_populates="pagamento"
    )


# ==================================================
# PIATTO
# ==================================================

class Piatto(Base):
    __tablename__ = "piatto"

    idPiatto: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    kcal: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    carboidrati: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False
    )

    proteine: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False
    )

    grassi: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False
    )

    prezzo: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "kcal >= 0",
            name="ck_piatto_kcal"
        ),
        CheckConstraint(
            "carboidrati >= 0",
            name="ck_piatto_carboidrati"
        ),
        CheckConstraint(
            "proteine >= 0",
            name="ck_piatto_proteine"
        ),
        CheckConstraint(
            "grassi >= 0",
            name="ck_piatto_grassi"
        ),
        CheckConstraint(
            "prezzo >= 0",
            name="ck_piatto_prezzo"
        ),
    )

    ordini: Mapped[list["OrdinePiatto"]] = relationship(
        back_populates="piatto"
    )


# ==================================================
# ORDINE
# ==================================================

class Ordine(Base):
    __tablename__ = "ordine"

    idOrdine: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    numOrdine: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False
    )

    dataOrdine: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    statoOrdine: Mapped[str] = mapped_column(
        String(30),
        server_default="in_attesa",
        nullable=False
    )

    idUtente: Mapped[int] = mapped_column(
        ForeignKey("utente.idUtente"),
        nullable=False
    )

    idCucina: Mapped[int] = mapped_column(
        ForeignKey("cucina.idCucina"),
        nullable=False
    )

    idPagamento: Mapped[int | None] = mapped_column(
        ForeignKey("pagamento.idPagamento"),
        unique=True,
        nullable=True
    )

    idRider: Mapped[int | None] = mapped_column(
        ForeignKey("rider.idRider"),
        nullable=True
    )

    # Relazione N:1 con Utente
    utente: Mapped["Utente"] = relationship(
        back_populates="ordini"
    )

    # Relazione N:1 con Cucina
    cucina: Mapped["Cucina"] = relationship(
        back_populates="ordini"
    )

    # Relazione 1:1 con Pagamento
    pagamento: Mapped["Pagamento | None"] = relationship(
        back_populates="ordine"
    )

    # Relazione N:1 con Rider
    rider: Mapped["Rider | None"] = relationship(
        back_populates="ordini"
    )

    # Relazione 1:N con OrdinePiatto
    piatti: Mapped[list["OrdinePiatto"]] = relationship(
        back_populates="ordine"
    )


# ==================================================
# ORDINE_PIATTO
# Associazione N:M con attributi
# ==================================================

class OrdinePiatto(Base):
    __tablename__ = "ordine_piatto"

    idOrdine: Mapped[int] = mapped_column(
        ForeignKey("ordine.idOrdine"),
        primary_key=True
    )

    idPiatto: Mapped[int] = mapped_column(
        ForeignKey("piatto.idPiatto"),
        primary_key=True
    )

    quantita: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    __table_args__ = (
        CheckConstraint(
            "quantita > 0",
            name="ck_ordine_piatto_quantita"
        ),
    )

    ordine: Mapped["Ordine"] = relationship(
        back_populates="piatti"
    )

    piatto: Mapped["Piatto"] = relationship(
        back_populates="ordini"
    )