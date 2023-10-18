from datetime import date

############################################################################
how_many_days_to_plot = 30
max_qty_assets_to_plot = 50
last_date = date.today()
how_many_calendar_days_of_data_to_fetch = how_many_days_to_plot + 60 # should be enough in most cases


############################################################################
indicator_name_parameters = {
  'MACD': dict(fast=12, slow=26, signal_period=9),
  'Stochastic': dict(period=3, k_period=14, level_top=90.0, level_bottom=10.0)
}
unnecessary_column_names = ['Data Date']

############################################################################
all_tickers = ["000001.SS", "AAPL", 
  "AAZ.L", "AD.AS", "AE9.F", "AG", "AMAT", "AMD", "AMGN", "AMPS", "ATG.L"]#,
["AUTO.L", "AV.L", "AZN", "BCS", "BDEV.L", "BHC", "BHP", "BP", "BRBR", "BTI",  "BUR", "C", "CF.TO", "CHMI", "CNA.L", "CO.PA", "COLR.BR", "CRH", "CVS",
  "CVX", "CWK.L", "DAX", "DBC", "DEO", "DI6.DU", "DIS", "DNLI", "DRO.AX",
  "EVA", "EVN.AX", "EZJ.L", "FAST", "FCX", "FERG", "FNMA", "FNV", "GE",
  "GFTU.L", "GILD", "GLD.JO", "GOLD", "GRG.L", "GSK", "GWW", "HEAD.L", "HL",
  "HSBC", "HVO.L", "IDS.L", "IMPP", "INR.SG", "INTC", "ITRK.L", "JD", "JRONY", "KEUA", "KIE.L", "KLA.SG", "KR", "LOOK.L", "LSEG.L", "MAB.L", "MMM",
  "NAC", "NEM", "NST.AX", "NWL", "OILUSA.SW", "OPTI.L", "OXY", "PDG.L", "PFE",
  "POST", "PSHZF", "QCOM", "RIO", "RS", "RXL.PA", "RYCEY", "SAGE", "SBRY.L",
  "SCCO", "SDY.L", "SMPL", "SOYB.L", "SPOT", "SRP.L", "TGA.JO", "TLSA",
  "TPK.L", "TRN.L", "TSCO.L", "TSLA", "U-UN.TO", "UJO.L", "UL", "UNG", "URA",
  "VOD", "VRS.L", "VTU.L", "VZ", "WBX", "WCC", "WG.L", "WH", "WMT", "WSO",
  "WTB.L", "XTRA.TO", "YINN"]

# ['TSCO.L', 'SANOFI.NS', "LLOY.L", 'AAPL']
# FAILURES: "0LKC.IL", "280930.KS",

############################################################################
max_digits_for_price = 5
plot_height_inches = 6
max_title_length = 50
folder_for_files = 'files_with_numbers'
plot_filename = "plots_StochMACDuck.jpg"
excel_filename = "excel_StochMACDuck"
info_filename = 'info_df'
tickers_long_names_filename = 'tickers_long_names'
last_date_filename = 'last_date_data'
# colors: https://matplotlib.org/stable/gallery/color/named_colors.html
# linestyles: https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
chart_color = {
  'stochD': 'blue',
  'stochK': ['magenta', 'dotted'],
  'level_bottom': ['black', 'dashed'],
  'level_top': ['black', 'dashed'],
  'MACD': 'orange',
  'signal': 'cyan',
  'histogram': 'black',
  'stock_green': 'green',
  'stock_red': 'red',
  'stock_mid': 'none'
}