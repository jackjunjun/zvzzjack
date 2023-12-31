.. _adding_new_entity:

=================
Adding new entity
=================

It's human nature to like the new and hate the old. Adding new TradableEntity is easy in zvt.

Adding new entity is nothing than a specific case of :ref:`Adding data <extending_data.add_data>`.
Let's show the key steps below which add :class:`~.zvt.domain.meta.future_meta.Future`.

Define entity Schema
--------------------------

::

    # -*- coding: utf-8 -*-
    from sqlalchemy.ext.declarative import declarative_base

    from zvt.contract.register import register_schema, register_entity
    from zvt.contract.schema import TradableEntity

    FutureMetaBase = declarative_base()


    @register_entity(entity_type="future")
    class Future(FutureMetaBase, TradableEntity):
        __tablename__ = "future"


    register_schema(providers=["em"], db_name="future_meta", schema_base=FutureMetaBase)

Implement recorder for the entity
---------------------------------

::

    from zvt.contract.api import df_to_db
    from zvt.contract.recorder import Recorder
    from zvt.domain import Future
    from zvt.recorders.em import em_api


    class EMFutureRecorder(Recorder):
        provider = "em"
        data_schema = Future

        def run(self):
            df = em_api.get_tradable_list(entity_type="future")
            self.logger.info(df)
            df_to_db(df=df, data_schema=self.data_schema, provider=self.provider, force_update=self.force_update)


Define OHLC schema(kdata) for the entity
----------------------------------------

zvt provide a standard way to generate OHLC schema for the tradable entity.
All `OHLC schemas <https://github.com/zvtvz/zvt/blob/master/src/zvt/domain/quotes>`_ is generated by
`fill project script <https://github.com/zvtvz/zvt/blob/master/src/zvt/fill_project.py>`_.

e.g generate Future OHLC schema.

::

    gen_kdata_schema(
        pkg="zvt",
        providers=["em"],
        entity_type="future",
        levels=[IntervalLevel.LEVEL_1DAY],
        entity_in_submodule=True,
    )

The OHLC schema definition principle is: **one level one file**

So we would define a common OHLC schema for each entity type in `quotes module <https://github.com/zvtvz/zvt/blob/master/src/zvt/domain/quotes/__init__.py>`_.

e.g. Future common OHLC schema

::

    class FutureKdataCommon(KdataCommon):
        #: 持仓量
        interest = Column(Float)
        #: 结算价
        settlement = Column(Float)
        #: 涨跌幅(按收盘价)
        # change_pct = Column(Float)
        #: 涨跌幅(按结算价)
        change_pct1 = Column(Float)

And we could relate the common kdata schema with the recorder and route level to specific schema automatically.

Implement recorder for OHLC schema(kdata)
-----------------------------------------

Check `em quotes recorder <https://github.com/zvtvz/zvt/blob/master/src/zvt/recorders/em/quotes/em_kdata_recorder.py>`_ for
the details.

::

    class EMFutureKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Future

    data_schema = FutureKdataCommon


Use them in zvt way
-------------------

Fetch the entity list:

::

    >>> from zvt.domain import Future
    >>> Future.record_data()
    >>> df = Future.query_data()
    >>> print(df)

                     id        entity_id  timestamp entity_type exchange code    name  list_date end_date
    0   future_cffex_IC  future_cffex_IC        NaT      future    cffex   IC  中证当月连续        NaT     None
    1   future_cffex_IF  future_cffex_IF        NaT      future    cffex   IF  沪深当月连续        NaT     None
    2   future_cffex_IH  future_cffex_IH        NaT      future    cffex   IH  上证当月连续        NaT     None
    3    future_cffex_T   future_cffex_T        NaT      future    cffex    T  十债当季连续        NaT     None
    4   future_cffex_TF  future_cffex_TF        NaT      future    cffex   TF  五债当季连续        NaT     None
    ..              ...              ...        ...         ...      ...  ...     ...        ...      ...
    65    future_ine_LU    future_ine_LU 2020-06-22      future      ine   LU  低硫燃油主力 2020-06-22     None
    66   future_czce_PF   future_czce_PF 2020-10-12      future     czce   PF    短纤主力 2020-10-12     None
    67    future_ine_BC    future_ine_BC 2020-11-19      future      ine   BC   国际铜主力 2020-11-19     None
    68    future_dce_LH    future_dce_LH 2021-01-08      future      dce   LH    生猪主力 2021-01-08     None
    69   future_czce_PK   future_czce_PK 2021-02-01      future     czce   PK    花生主力 2021-02-01     None

    [70 rows x 9 columns]

Fetch the quotes:

::

    >>> from zvt.domain import Future1dKdata
    >>> Future1dKdata.record_data(code="CU")
    >>> df = Future1dKdata.query_data(code="CU")
    >>> print(df)

                                 id       entity_id  timestamp provider code  name level     open    close     high      low    volume      turnover  change_pct  turnover_rate interest settlement change_pct1
    0     future_shfe_CU_1996-04-03  future_shfe_CU 1996-04-03       em   CU  沪铜主力    1d  22930.0  22840.0  23000.0  22840.0     353.0  0.000000e+00      0.0000            0.0     None       None        None
    1     future_shfe_CU_1996-04-04  future_shfe_CU 1996-04-04       em   CU  沪铜主力    1d  22700.0  22750.0  22820.0  22650.0     251.0  0.000000e+00     -0.0039            0.0     None       None        None
    2     future_shfe_CU_1996-04-05  future_shfe_CU 1996-04-05       em   CU  沪铜主力    1d  22520.0  22780.0  22820.0  22500.0     298.0  0.000000e+00      0.0013            0.0     None       None        None
    3     future_shfe_CU_1996-04-08  future_shfe_CU 1996-04-08       em   CU  沪铜主力    1d  22660.0  22650.0  22680.0  22600.0      98.0  0.000000e+00     -0.0057            0.0     None       None        None
    4     future_shfe_CU_1996-04-09  future_shfe_CU 1996-04-09       em   CU  沪铜主力    1d  22830.0  22810.0  22860.0  22810.0      56.0  0.000000e+00      0.0071            0.0     None       None        None
    ...                         ...             ...        ...      ...  ...   ...   ...      ...      ...      ...      ...       ...           ...         ...            ...      ...        ...         ...
    6343  future_shfe_CU_2022-04-21  future_shfe_CU 2022-04-21       em   CU  沪铜主力    1d  74140.0  74480.0  74750.0  74140.0   48008.0  1.787678e+10     -0.0004            0.0     None       None        None
    6344  future_shfe_CU_2022-04-22  future_shfe_CU 2022-04-22       em   CU  沪铜主力    1d  74800.0  75010.0  75200.0  74690.0   58874.0  2.205633e+10      0.0073            0.0     None       None        None
    6345  future_shfe_CU_2022-04-25  future_shfe_CU 2022-04-25       em   CU  沪铜主力    1d  74900.0  73660.0  75190.0  73660.0  107455.0  3.989090e+10     -0.0168            0.0     None       None        None
    6346  future_shfe_CU_2022-04-26  future_shfe_CU 2022-04-26       em   CU  沪铜主力    1d  73170.0  73260.0  73750.0  72500.0  113019.0  4.130931e+10     -0.0132            0.0     None       None        None
    6347  future_shfe_CU_2022-04-27  future_shfe_CU 2022-04-27       em   CU  沪铜主力    1d  72990.0  73100.0  73560.0  72910.0   61563.0  2.254089e+10      0.0000            0.0     None       None        None

    [6348 rows x 18 columns]
