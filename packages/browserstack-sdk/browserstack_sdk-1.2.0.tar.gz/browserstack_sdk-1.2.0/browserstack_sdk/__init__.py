# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack1l1_opy_ = 7
def bstack1l_opy_ (bstack1l1l_opy_):
    global bstackl_opy_
    bstack1ll_opy_ = ord (bstack1l1l_opy_ [-1])
    bstack1ll1_opy_ = bstack1l1l_opy_ [:-1]
    bstack1lll_opy_ = bstack1ll_opy_ % len (bstack1ll1_opy_)
    bstack111_opy_ = bstack1ll1_opy_ [:bstack1lll_opy_] + bstack1ll1_opy_ [bstack1lll_opy_:]
    if bstack1l11_opy_:
        bstack11_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack11l_opy_ + bstack1ll_opy_) % bstack1l1_opy_) for bstack11l_opy_, char in enumerate (bstack111_opy_)])
    else:
        bstack11_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack11l_opy_ + bstack1ll_opy_) % bstack1l1_opy_) for bstack11l_opy_, char in enumerate (bstack111_opy_)])
    return eval (bstack11_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
from packaging import version
from browserstack.local import Local
bstack1llll1_opy_ = {
	bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫৌ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ্ࠧ"),
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧৎ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ৏"),
  bstack1l_opy_ (u"࠭࡯ࡴࠩ৐"): bstack1l_opy_ (u"ࠧࡰࡵࠪ৑"),
  bstack1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ৒"): bstack1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭৓"),
  bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ৔"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ৕"),
  bstack1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ৖"): bstack1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧৗ"),
  bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ৘"): bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧ৙"),
  bstack1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ৚"): bstack1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ৛"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪড়"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪঢ়"),
  bstack1l_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫ৞"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧয়"),
  bstack1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ৠ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ৡ"),
  bstack1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧৢ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧৣ"),
  bstack1l_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫ৤"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫ৥"),
  bstack1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭০"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭১"),
  bstack1l_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ২"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩ৩"),
  bstack1l_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ৪"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩ৫"),
  bstack1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ৬"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨ৭"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷࡴࡲࡵࡵ࡫ࡲࡲࠬ৮"): bstack1l_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭৯"),
  bstack1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬৰ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৱ"),
  bstack1l_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫ৲"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫ৳"),
  bstack1l_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬ৴"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬ৵"),
  bstack1l_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ৶"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ৷"),
  bstack1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭৸"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭৹"),
  bstack1l_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ৺"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ৻"),
  bstack1l_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧৼ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡹࠧ৽"),
  bstack1l_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫ৾"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦ࡫ࡩࡡࡤࡪࡨࠫ৿"),
  bstack1l_opy_ (u"ࠬࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭਀"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡽࡳࡍࡱࡦࡥࡱ࡙ࡵࡱࡲࡲࡶࡹ࠭ਁ"),
  bstack1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪਂ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥ࡫ࡶࡥࡧࡲࡥࡄࡱࡵࡷࡗ࡫ࡳࡵࡴ࡬ࡧࡹ࡯࡯࡯ࡵࠪਃ"),
  bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭਄"): bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪਅ"),
  bstack1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨਆ"): bstack1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪਇ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ਈ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧਉ"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬਊ"): bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭਋"),
  bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪ਌"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪ਍"),
  bstack1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭਎"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ਏ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ਐ"): bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩ਑"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ਒"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫਓ"),
  bstack1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫਔ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸࡵࡵࡳࡥࡨࠫਕ"),
  bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਖ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨਗ"),
  bstack1l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪਘ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡔࡡ࡮ࡧࠪਙ"),
}
bstack1111_opy_ = [
  bstack1l_opy_ (u"ࠪࡳࡸ࠭ਚ"),
  bstack1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧਛ"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧਜ"),
  bstack1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਝ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫਞ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬਟ"),
  bstack1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩਠ"),
]
bstack1l11l_opy_ = {
  bstack1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ਡ"): bstack1l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਢ"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧਣ"): [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਤ"), bstack1l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪਥ")],
  bstack1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਦ"): bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧਧ"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧਨ"): bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ਩"),
  bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪਪ"): [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧਫ"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ਬ")],
  bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩਭ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫਮ"),
  bstack1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧਯ"): bstack1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩਰ"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ਱"): [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ਲ"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨਲ਼")],
  bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧ਴"): [bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪਵ"), bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࠪਸ਼")]
}
bstack11l11_opy_ = {
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ਷"): [bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ਸ"), bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭ਹ")]
}
bstack1l1l1_opy_ = [
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭਺"),
  bstack1l_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫ਻"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ਼"),
  bstack1l_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶࠪ਽"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ਾ"),
  bstack1l_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻࠪਿ"),
  bstack1l_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩੀ"),
  bstack1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬੁ"),
  bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ੂ"),
  bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ੃"),
  bstack1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੄"),
  bstack1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ੅"),
]
bstack1l1ll_opy_ = [
  bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ੆"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪੇ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ੈ"),
  bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੉"),
  bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊"),
  bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬੋ"),
  bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧੌ"),
  bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺ੍ࠩ"),
  bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ੎"),
]
bstack111ll_opy_ = [
  bstack1l_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬ੏"),
  bstack1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੐"),
  bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬੑ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੒"),
  bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪ੓"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ੔"),
  bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨ੕"),
  bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ੖"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ੗"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ੘"),
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਖ਼"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪਗ਼"),
  bstack1l_opy_ (u"ࠬࡵࡳࠨਜ਼"),
  bstack1l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩੜ"),
  bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭੝"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪਫ਼"),
  bstack1l_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩ੟"),
  bstack1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬ੠"),
  bstack1l_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬ੡"),
  bstack1l_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩ੢"),
  bstack1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫ੣"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫ੤"),
  bstack1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧ੥"),
  bstack1l_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭੦"),
  bstack1l_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫ੧"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ੨"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ੩"),
  bstack1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ੪"),
  bstack1l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ੫"),
  bstack1l_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬ੬"),
  bstack1l_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫ੭"),
  bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੮"),
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫ੯"),
  bstack1l_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫੰ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪੱ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧੲ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲࠬੳ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩࠪੴ"),
  bstack1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴࠩੵ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ੶"),
  bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪࠧ੷"),
  bstack1l_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨ੸"),
  bstack1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭੹"),
  bstack1l_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭੺"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧ੻"),
  bstack1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨ੼"),
  bstack1l_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩ੽"),
  bstack1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ੾"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪ੿"),
  bstack1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩ઀"),
  bstack1l_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩઁ"),
  bstack1l_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪં"),
  bstack1l_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫઃ"),
  bstack1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪ઄"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪઅ"),
  bstack1l_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭આ"),
  bstack1l_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࠩઇ"),
  bstack1l_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ઈ"),
  bstack1l_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧઉ"),
  bstack1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࠫઊ"),
  bstack1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫઋ"),
  bstack1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ઌ"),
  bstack1l_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷ࠭ઍ"),
  bstack1l_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧ઎"),
  bstack1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧએ"),
  bstack1l_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩઐ"),
  bstack1l_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫઑ"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹࠧ઒"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯ࠩઓ"),
  bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬઔ"),
  bstack1l_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࠪક"),
  bstack1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࠬખ"),
  bstack1l_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩગ"),
  bstack1l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫઘ"),
  bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫઙ"),
  bstack1l_opy_ (u"ࠬ࡯ࡥࠨચ"),
  bstack1l_opy_ (u"࠭ࡥࡥࡩࡨࠫછ"),
  bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧજ"),
  bstack1l_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࠧઝ"),
  bstack1l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫઞ"),
  bstack1l_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫટ"),
  bstack1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪઠ"),
  bstack1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨડ"),
  bstack1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩઢ"),
  bstack1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫણ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨત"),
  bstack1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩથ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬદ"),
  bstack1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬધ"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡻࡤࡪࡱࡌࡲ࡯࡫ࡣࡵ࡫ࡲࡲࠬન"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ઩"),
  bstack1l_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬપ"),
  bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪફ"),
  bstack1l_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭બ"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧભ"),
  bstack1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧમ"),
  bstack1l_opy_ (u"ࠬࡸࡥ࡮ࡱࡹࡩࡎࡕࡓࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࡑࡵࡣࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪય"),
  bstack1l_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨર"),
  bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ઱")
]
bstack11l1_opy_ = {
  bstack1l_opy_ (u"ࠨࡸࠪલ"): bstack1l_opy_ (u"ࠩࡹࠫળ"),
  bstack1l_opy_ (u"ࠪࡪࠬ઴"): bstack1l_opy_ (u"ࠫ࡫࠭વ"),
  bstack1l_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࠫશ"): bstack1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬષ"),
  bstack1l_opy_ (u"ࠧࡰࡰ࡯ࡽࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭સ"): bstack1l_opy_ (u"ࠨࡱࡱࡰࡾࡇࡵࡵࡱࡰࡥࡹ࡫ࠧહ"),
  bstack1l_opy_ (u"ࠩࡩࡳࡷࡩࡥ࡭ࡱࡦࡥࡱ࠭઺"): bstack1l_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧ઻"),
  bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺ઼ࠧ"): bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨઽ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩા"): bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪિ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫી"): bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬુ"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡤࡷࡸ࠭ૂ"): bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧૃ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡪࡲࡷࡹ࠭ૄ"): bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡋࡳࡸࡺࠧૅ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡴࡸࡴࠨ૆"): bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡵࡲࡵࠩે"),
  bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪૈ"): bstack1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬૉ"),
  bstack1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭૊"): bstack1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧો"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧૌ"): bstack1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴ્ࠩ"),
  bstack1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪ૎"): bstack1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫ૏"),
  bstack1l_opy_ (u"ࠪࡦ࡮ࡴࡡࡳࡻࡳࡥࡹ࡮ࠧૐ"): bstack1l_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨ૑"),
  bstack1l_opy_ (u"ࠬࡶࡡࡤࡨ࡬ࡰࡪ࠭૒"): bstack1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ૓"),
  bstack1l_opy_ (u"ࠧࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ૔"): bstack1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ૕"),
  bstack1l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ૖"): bstack1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭૗"),
  bstack1l_opy_ (u"ࠫࡱࡵࡧࡧ࡫࡯ࡩࠬ૘"): bstack1l_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭૙"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૚"): bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૛"),
}
bstack1llll_opy_ = bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡺࡨ࠴࡮ࡵࡣࠩ૜")
bstack11ll_opy_ = bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠬ૝")
bstack111l_opy_ = {
  bstack1l_opy_ (u"ࠪࡧࡷ࡯ࡴࡪࡥࡤࡰࠬ૞"): 50,
  bstack1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ૟"): 40,
  bstack1l_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ૠ"): 30,
  bstack1l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫૡ"): 20,
  bstack1l_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ૢ"): 10
}
DEFAULT_LOG_LEVEL = bstack111l_opy_[bstack1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ૣ")]
bstack1ll11_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૤")
bstack11l1l_opy_ = bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૥")
bstack1lll11_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪ૦")
bstack11111_opy_ = [bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭૧"), bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭૨")]
bstack1lll1l_opy_ = [bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ૩"), bstack1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ૪")]
bstack1ll1l_opy_ = [
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૫"),
  bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૬"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ૭"),
  bstack1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩ૮"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲࠪ૯"),
  bstack1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬ૰"),
  bstack1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ૱"),
  bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩ૲"),
  bstack1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨ૳"),
  bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩ૴"),
  bstack1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭૵"), bstack1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩ૶"),
  bstack1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪ૷"),
  bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧ૸"),
  bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ૹ"),
  bstack1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭ૺ"),
  bstack1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬૻ"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪૼ"), bstack1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ૽"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ૾"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ૿"), bstack1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ଀"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨଁ"),
  bstack1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨଂ"),
  bstack1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧଃ"), bstack1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ଄"),
  bstack1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬଅ"),
  bstack1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩଆ"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨଇ"),
  bstack1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫଈ"),
  bstack1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩଉ"),
  bstack1l_opy_ (u"ࠬࡧࡶࡥࠩଊ"), bstack1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩଋ"), bstack1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩଌ"), bstack1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩ଍"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧ଎"), bstack1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩଏ"), bstack1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧଐ"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧ଑"), bstack1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫ଒"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩଓ"), bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫଔ"), bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧକ"), bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬଖ"), bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨଗ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨଘ"), bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪଙ"),
  bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩଚ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ଛ"),
  bstack1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨଜ"), bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫଝ"), bstack1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩଞ"), bstack1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨଟ"),
  bstack1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫଠ"),
  bstack1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩଡ"), bstack1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨଢ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩଣ"),
  bstack1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬତ"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭ଥ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬଦ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧଧ"),
  bstack1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ନ"),
  bstack1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩ଩"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨପ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧଫ"),
  bstack1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨବ"),
  bstack1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ଭ"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬମ"),
  bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫଯ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨର"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ଱"),
  bstack1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧଲ"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫଳ"),
  bstack1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩ଴"), bstack1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪଵ"), bstack1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪଶ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬଷ"),
  bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ସ"),
  bstack1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬହ"),
  bstack1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭଺"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ଻"),
  bstack1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮଼ࠪ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪଽ"), bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧା"), bstack1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬି"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪୀ"),
  bstack1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬୁ"),
  bstack1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧୂ"),
  bstack1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ୃ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪୄ"), bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧ୅"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬ୆"), bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧେ"),
  bstack1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫୈ"),
  bstack1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ୉"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ୊"), bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫୋ"), bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬୌ"), bstack1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥ୍ࠩ"),
  bstack1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪ୎"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬ୏"),
  bstack1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ୐"),
  bstack1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭୑"),
  bstack1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪࠫ୒"),
  bstack1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪ୓"),
  bstack1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪ୔"), bstack1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫ୕"),
  bstack1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧୖ"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬୗ"),
  bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧ୘"),
  bstack1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ୙"),
  bstack1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪ୚"),
  bstack1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ୛"),
  bstack1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫଡ଼"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬଢ଼"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬ୞"),
  bstack1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫୟ"),
  bstack1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬୠ"),
  bstack1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧୡ"),
  bstack1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨୢ"),
  bstack1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩࠬୣ"),
  bstack1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭୤"),
  bstack1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ୥"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ୦"),
  bstack1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ୧"),
  bstack1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ୨"),
  bstack1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ୩"),
  bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭୪"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ୫"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ୬"),
  bstack1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪ୭"), bstack1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ୮"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭୯"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ୰"),
  bstack1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬୱ"),
  bstack1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨ୲"), bstack1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨ୳"),
  bstack1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ୴"),
  bstack1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬ୵"),
  bstack1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨ୶"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪ୷"),
  bstack1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬ୸"),
  bstack1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧ୹"),
  bstack1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ୺"),
  bstack1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ୻"),
  bstack1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ୼"),
  bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ୽"), bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭୾"),
  bstack1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ୿")
]
bstack111l1_opy_ = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ஀")
bstack1l111_opy_ = [bstack1l_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ஁"), bstack1l_opy_ (u"࠭࠮ࡢࡣࡥࠫஂ"), bstack1l_opy_ (u"ࠧ࠯࡫ࡳࡥࠬஃ")]
bstack11ll1_opy_ = [bstack1l_opy_ (u"ࠨ࡫ࡧࠫ஄"), bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧஅ"), bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ஆ"), bstack1l_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪஇ")]
bstack11lll_opy_ = {
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬஈ"): bstack1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫஉ"),
  bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨஊ"): bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭஋"),
  bstack1l_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ஌"): bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ஍"),
  bstack1l_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧஎ"): bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫஏ"),
  bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭ஐ"): bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ஑")
}
bstack1lllll_opy_ = [
  bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ஒ"),
  bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧஓ"),
  bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫஔ"),
  bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪக"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭஖"),
]
bstack1111l_opy_ = bstack1l1ll_opy_ + bstack111ll_opy_ + bstack1ll1l_opy_
bstack11ll1l11_opy_ = bstack1l_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭஗")
bstack1ll1l1l1_opy_ = bstack1l_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪ஘")
bstack11lll11l_opy_ = bstack1l_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪங")
bstack11ll1111_opy_ = bstack1l_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧச")
bstack1l1l111l_opy_ = bstack1l_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ஛")
bstack111lll1l_opy_ = bstack1l_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫஜ")
bstack111l1l_opy_ = bstack1l_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬ஝")
bstack1ll1lll1_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫஞ")
bstack11l1l11l_opy_ = bstack1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬட")
bstack11l1ll1_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡵࡳࡧࡵࡴ࠭ࠢࡳࡥࡧࡵࡴࠡࡣࡱࡨࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡷࡳࠥࡸࡵ࡯ࠢࡵࡳࡧࡵࡴࠡࡶࡨࡷࡹࡹࠠࡪࡰࠣࡴࡦࡸࡡ࡭࡮ࡨࡰ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡱࡣࡥࡳࡹࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࡢࠪ஠")
bstack1ll11111_opy_ = bstack1l_opy_ (u"ࠩࡋࡥࡳࡪ࡬ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡬ࡰࡵࡨࠫ஡")
bstack1ll1ll1l_opy_ = bstack1l_opy_ (u"ࠪࡅࡱࡲࠠࡥࡱࡱࡩࠦ࠭஢")
bstack11lll11_opy_ = bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࠣࡥࡹࠦࠢࡼࡿࠥ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦࠢࡦࡳࡳࡺࡡࡪࡰ࡬࡫ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࡳ࠯ࠩண")
bstack11lllll_opy_ = bstack1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡸࡥࡥࡧࡱࡸ࡮ࡧ࡬ࡴࠢࡱࡳࡹࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠢࡓࡰࡪࡧࡳࡦࠢࡤࡨࡩࠦࡴࡩࡧࡰࠤ࡮ࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥࠡࡣࡶࠤࠧࡻࡳࡦࡴࡑࡥࡲ࡫ࠢࠡࡣࡱࡨࠥࠨࡡࡤࡥࡨࡷࡸࡑࡥࡺࠤࠣࡳࡷࠦࡳࡦࡶࠣࡸ࡭࡫࡭ࠡࡣࡶࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷ࠿ࠦࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣࠢࡤࡲࡩࠦࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠥࠫத")
bstack1l1lll1_opy_ = bstack1l_opy_ (u"࠭ࡍࡢ࡮ࡩࡳࡷࡳࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠣࡽࢀࠦࠬ஥")
bstack1llllll_opy_ = bstack1l_opy_ (u"ࠧࡆࡰࡦࡳࡺࡴࡴࡦࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠ࠮ࠢࡾࢁࠬ஦")
bstack1ll111ll_opy_ = bstack1l_opy_ (u"ࠨࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠨ஧")
bstack1l1l1l11_opy_ = bstack1l_opy_ (u"ࠩࡖࡸࡴࡶࡰࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭ࠩந")
bstack1l1ll1_opy_ = bstack1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬ࠡ࡫ࡶࠤࡳࡵࡷࠡࡴࡸࡲࡳ࡯࡮ࡨࠣࠪன")
bstack1l111ll1_opy_ = bstack1l_opy_ (u"ࠫࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡴࡶࡤࡶࡹࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯࠾ࠥࢁࡽࠨப")
bstack11111ll1_opy_ = bstack1l_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠ࡭ࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦࡷࡪࡶ࡫ࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࡻࡾࠩ஫")
bstack111111ll_opy_ = bstack1l_opy_ (u"࠭ࡕࡱࡦࡤࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠧ஬")
bstack1l1l1ll_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂ࠭஭")
bstack11l11ll1_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࠢࡤࡲࠥࡧࡰࡱࡴࡲࡴࡷ࡯ࡡࡵࡧࠣࡊ࡜ࠦࠨࡳࡱࡥࡳࡹ࠵ࡰࡢࡤࡲࡸ࠮ࠦࡩ࡯ࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠬࠡࡵ࡮࡭ࡵࠦࡴࡩࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡫ࡦࡻࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡩࡧࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡷ࡮ࡳࡰ࡭ࡧࠣࡴࡾࡺࡨࡰࡰࠣࡷࡨࡸࡩࡱࡶࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡦࡴࡹࠡࡈ࡚࠲ࠬம")
bstack111lllll_opy_ = bstack1l_opy_ (u"ࠩࡖࡩࡹࡺࡩ࡯ࡩࠣ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠵ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦ࡯࡯ࠢࡦࡹࡷࡸࡥ࡯ࡶ࡯ࡽࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡲࡪࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࠩࡽࢀ࠭࠱ࠦࡰ࡭ࡧࡤࡷࡪࠦࡵࡱࡩࡵࡥࡩ࡫ࠠࡵࡱࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡃࡃ࠴࠯࠲࠱࠴ࠥࡵࡲࠡࡴࡨࡪࡪࡸࠠࡵࡱࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠵ࡲࡶࡰ࠰ࡸࡪࡹࡴࡴ࠯ࡥࡩ࡭࡯࡮ࡥ࠯ࡳࡶࡴࡾࡹࠤࡲࡼࡸ࡭ࡵ࡮ࠡࡨࡲࡶࠥࡧࠠࡸࡱࡵ࡯ࡦࡸ࡯ࡶࡰࡧ࠲ࠬய")
bstack1l1llll1_opy_ = bstack1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠯࠰ࠪர")
bstack11ll111_opy_ = bstack1l_opy_ (u"ࠫࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࡩࠦࡴࡩࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠢࠩற")
bstack11l1ll11_opy_ = bstack1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡪ࡮ࡨ࠲ࠥࢁࡽࠨல")
bstack1ll1111_opy_ = bstack1l_opy_ (u"࠭ࡅࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡷࠤࡱ࡫ࡡࡴࡶࠣ࠵ࠥ࡯࡮ࡱࡷࡷ࠰ࠥࡸࡥࡤࡧ࡬ࡺࡪࡪࠠ࠱ࠩள")
bstack1l1lll11_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡁࡱࡲࠣࡹࡵࡲ࡯ࡢࡦ࠱ࠤࢀࢃࠧழ")
bstack11l1l1l1_opy_ = bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡆࡶࡰ࠯ࠢࡌࡲࡻࡧ࡬ࡪࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡽࢀ࠲ࠬவ")
bstack111ll1l_opy_ = bstack1l_opy_ (u"ࠩࡎࡩࡾࡹࠠࡤࡣࡱࡲࡴࡺࠠࡤࡱ࠰ࡩࡽ࡯ࡳࡵࠢࡤࡷࠥࡧࡰࡱࠢࡹࡥࡱࡻࡥࡴ࠮ࠣࡹࡸ࡫ࠠࡢࡰࡼࠤࡴࡴࡥࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࠣࡪࡷࡵ࡭ࠡࡽ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡱࡣࡷ࡬ࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂࢂ࠲ࠠࡰࡰ࡯ࡽࠥࠨࡰࡢࡶ࡫ࠦࠥࡧ࡮ࡥࠢࠥࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࠨࠠࡤࡣࡱࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡴࡰࡩࡨࡸ࡭࡫ࡲ࠯ࠩஶ")
bstack1111lll1_opy_ = bstack1l_opy_ (u"ࠪ࡟ࡎࡴࡶࡢ࡮࡬ࡨࠥࡧࡰࡱࠢࡳࡶࡴࡶࡥࡳࡶࡼࡡࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠥࡧࡲࡦࠢࡾ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡲࡤࡸ࡭ࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃࢃ࠮ࠡࡈࡲࡶࠥࡳ࡯ࡳࡧࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡵࡲࡥࡢࡵࡨࠤࡻ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳࡴ࡮ࡻ࡭࠰ࡵࡨࡸ࠲ࡻࡰ࠮ࡶࡨࡷࡹࡹ࠯ࡴࡲࡨࡧ࡮࡬ࡹ࠮ࡣࡳࡴࠬஷ")
bstack11l111_opy_ = bstack1l_opy_ (u"ࠫࡠࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡡࡱࡲࠣࡴࡷࡵࡰࡦࡴࡷࡽࡢࠦࡓࡶࡲࡳࡳࡷࡺࡥࡥࠢࡹࡥࡱࡻࡥࡴࠢࡲࡪࠥࡧࡰࡱࠢࡤࡶࡪࠦ࡯ࡧࠢࡾ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡲࡤࡸ࡭ࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃࢃ࠮ࠡࡈࡲࡶࠥࡳ࡯ࡳࡧࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡵࡲࡥࡢࡵࡨࠤࡻ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡩࡵࡣࡴ࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳࡴ࡮ࡻ࡭࠰ࡵࡨࡸ࠲ࡻࡰ࠮ࡶࡨࡷࡹࡹ࠯ࡴࡲࡨࡧ࡮࡬ࡹ࠮ࡣࡳࡴࠬஸ")
bstack111l111_opy_ = bstack1l_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡡࡱࡲࠣ࡭ࡩࠦࡻࡾࠢࡩࡳࡷࠦࡨࡢࡵ࡫ࠤ࠿ࠦࡻࡾ࠰ࠪஹ")
bstack11ll11ll_opy_ = bstack1l_opy_ (u"࠭ࡁࡱࡲ࡙ࠣࡵࡲ࡯ࡢࡦࡨࡨ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠥࡏࡄࠡ࠼ࠣࡿࢂ࠭஺")
bstack11l1111l_opy_ = bstack1l_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡁࡱࡲࠣ࠾ࠥࢁࡽ࠯ࠩ஻")
bstack1l11l1l_opy_ = bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡵࡲࠡࡸࡤࡲ࡮ࡲ࡬ࡢࠢࡳࡽࡹ࡮࡯࡯ࠢࡷࡩࡸࡺࡳ࠭ࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡻ࡮ࡺࡨࠡࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠠ࠾ࠢ࠴ࠫ஼")
bstack1lll1l1_opy_ = bstack1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠻ࠢࡾࢁࠬ஽")
from ._version import __version__
bstack1l1ll11_opy_ = None
CONFIG = {}
bstack11l1l1l_opy_ = None
bstack1111ll_opy_ = None
bstack1l1lll1l_opy_ = None
bstack1l1ll111_opy_ = -1
bstack1llllll1_opy_ = DEFAULT_LOG_LEVEL
bstack1l1l111_opy_ = 1
bstack11ll1l_opy_ = False
bstack1lll11l1_opy_ = bstack1l_opy_ (u"ࠪࠫா")
bstack1ll111l1_opy_ = bstack1l_opy_ (u"ࠫࠬி")
bstack1l1l11l_opy_ = False
bstack1111111_opy_ = None
bstack111ll111_opy_ = None
bstack1ll1ll1_opy_ = None
bstack1l11l1l1_opy_ = None
bstack11111lll_opy_ = None
bstack111ll1ll_opy_ = None
bstack1lll1111_opy_ = None
bstack1111111l_opy_ = None
bstack11ll11_opy_ = None
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1llllll1_opy_,
                    format=bstack1l_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪீ"),
                    datefmt=bstack1l_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨு"))
def bstack1111l11_opy_():
  global CONFIG
  global bstack1llllll1_opy_
  if bstack1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩூ") in CONFIG:
    bstack1llllll1_opy_ = bstack111l_opy_[CONFIG[bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ௃")]]
    logging.getLogger().setLevel(bstack1llllll1_opy_)
def bstack111ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1llll1l1_opy_():
  bstack111l1111_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ௄")
  bstack1lll1ll_opy_ = os.path.abspath(bstack111l1111_opy_)
  if not os.path.exists(bstack1lll1ll_opy_):
    bstack111l1111_opy_ = bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧ௅")
    bstack1lll1ll_opy_ = os.path.abspath(bstack111l1111_opy_)
    if not os.path.exists(bstack1lll1ll_opy_):
      bstack11l1ll_opy_(
        bstack11lll11_opy_.format(os.getcwd()))
  with open(bstack1lll1ll_opy_, bstack1l_opy_ (u"ࠫࡷ࠭ெ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11l1ll_opy_(bstack1l1lll1_opy_.format(str(exc)))
def bstack11ll1l1l_opy_(config):
  bstack11l11l1_opy_ = bstack1l11l1_opy_(config)
  for option in list(bstack11l11l1_opy_):
    if option.lower() in bstack11l1_opy_ and option != bstack11l1_opy_[option.lower()]:
      bstack11l11l1_opy_[bstack11l1_opy_[option.lower()]] = bstack11l11l1_opy_[option]
      del bstack11l11l1_opy_[option]
  return config
def bstack1l1lll_opy_(config):
  bstack1l11l11_opy_ = config.keys()
  for bstack1lll11l_opy_, bstack1lllll11_opy_ in bstack1llll1_opy_.items():
    if bstack1lllll11_opy_ in bstack1l11l11_opy_:
      config[bstack1lll11l_opy_] = config[bstack1lllll11_opy_]
      del config[bstack1lllll11_opy_]
  for bstack1lll11l_opy_, bstack1lllll11_opy_ in bstack11l11_opy_.items():
    for bstack1l111l1l_opy_ in bstack1lllll11_opy_:
      if bstack1l111l1l_opy_ in bstack1l11l11_opy_:
        config[bstack1lll11l_opy_] = config[bstack1l111l1l_opy_]
        del config[bstack1l111l1l_opy_]
  for bstack1l111l1l_opy_ in list(config):
    for bstack11l1lll_opy_ in bstack1111l_opy_:
      if bstack1l111l1l_opy_.lower() == bstack11l1lll_opy_.lower() and bstack1l111l1l_opy_ != bstack11l1lll_opy_:
        config[bstack11l1lll_opy_] = config[bstack1l111l1l_opy_]
        del config[bstack1l111l1l_opy_]
  bstack1lllll1l_opy_ = []
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨே") in config:
    bstack1lllll1l_opy_ = config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩை")]
  for platform in bstack1lllll1l_opy_:
    for bstack1l111l1l_opy_ in list(platform):
      for bstack11l1lll_opy_ in bstack1111l_opy_:
        if bstack1l111l1l_opy_.lower() == bstack11l1lll_opy_.lower() and bstack1l111l1l_opy_ != bstack11l1lll_opy_:
          platform[bstack11l1lll_opy_] = platform[bstack1l111l1l_opy_]
          del platform[bstack1l111l1l_opy_]
  for bstack1lll11l_opy_, bstack1lllll11_opy_ in bstack1l11l_opy_.items():
    for platform in bstack1lllll1l_opy_:
      if isinstance(bstack1lllll11_opy_, list):
        for bstack1l111l1l_opy_ in bstack1lllll11_opy_:
          if bstack1l111l1l_opy_ in platform:
            platform[bstack1lll11l_opy_] = platform[bstack1l111l1l_opy_]
            del platform[bstack1l111l1l_opy_]
            break
      elif bstack1lllll11_opy_ in platform:
        platform[bstack1lll11l_opy_] = platform[bstack1lllll11_opy_]
        del platform[bstack1lllll11_opy_]
  for bstack1lll11ll_opy_ in bstack11lll_opy_:
    if bstack1lll11ll_opy_ in config:
      if not bstack11lll_opy_[bstack1lll11ll_opy_] in config:
        config[bstack11lll_opy_[bstack1lll11ll_opy_]] = {}
      config[bstack11lll_opy_[bstack1lll11ll_opy_]].update(config[bstack1lll11ll_opy_])
      del config[bstack1lll11ll_opy_]
  for platform in bstack1lllll1l_opy_:
    for bstack1lll11ll_opy_ in bstack11lll_opy_:
      if bstack1lll11ll_opy_ in list(platform):
        if not bstack11lll_opy_[bstack1lll11ll_opy_] in platform:
          platform[bstack11lll_opy_[bstack1lll11ll_opy_]] = {}
        platform[bstack11lll_opy_[bstack1lll11ll_opy_]].update(platform[bstack1lll11ll_opy_])
        del platform[bstack1lll11ll_opy_]
  config = bstack11ll1l1l_opy_(config)
  return config
def bstack11llll11_opy_(config):
  global bstack1ll111l1_opy_
  if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ௉") in config and str(config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬொ")]).lower() != bstack1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨோ"):
    if not bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧௌ") in config:
      config[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ்")] = {}
    if not bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௎") in config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௏")]:
      if bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩௐ") in os.environ:
        config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ௑")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௒")] = os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ௓")]
      else:
        current_time = datetime.datetime.now()
        bstack1lllllll_opy_ = current_time.strftime(bstack1l_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨ௔"))
        hostname = socket.gethostname()
        bstack1llll1l_opy_ = bstack1l_opy_ (u"ࠬ࠭௕").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1l_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨ௖").format(bstack1lllllll_opy_, hostname, bstack1llll1l_opy_)
        config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫௗ")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௘")] = identifier
    bstack1ll111l1_opy_ = config[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௙")][bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௚")]
  return config
def bstack1llll111_opy_(config):
  if bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ௛") in config and config[bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ௜")] not in bstack1lll1l_opy_:
    return config[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௝")]
  elif bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ௞") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ௟")]
  else:
    return None
def bstack1l11111_opy_(config):
  if bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬ௠") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭௡")]
  elif bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௢") in config:
    return config[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௣")]
  else:
    return None
def bstack1lll111l_opy_():
  if (
    isinstance(os.getenv(bstack1l_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫ௤")), str) and len(os.getenv(bstack1l_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠬ௥"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧ௦")), str) and len(os.getenv(bstack1l_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠨ௧"))) > 0
  ):
    return os.getenv(bstack1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩ௨"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠫࡈࡏࠧ௩"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ௪") and str(os.getenv(bstack1l_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡉࡉࠨ௫"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ௬"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠫ௭"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࠬ௮"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ௯") and str(os.getenv(bstack1l_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࠫ௰"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ௱"):
    return os.getenv(bstack1l_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ௲"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪ௳"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭௴") and str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࡤࡔࡁࡎࡇࠪ௵"))).lower() == bstack1l_opy_ (u"ࠪࡧࡴࡪࡥࡴࡪ࡬ࡴࠬ௶"):
    return 0 # bstack11l11l1l_opy_ bstack1lllll1_opy_ not set build number env
  if os.getenv(bstack1l_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠧ௷")) and os.getenv(bstack1l_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠨ௸")):
    return os.getenv(bstack1l_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨ௹"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪ௺"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭௻") and str(os.getenv(bstack1l_opy_ (u"ࠩࡇࡖࡔࡔࡅࠨ௼"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ௽"):
    return os.getenv(bstack1l_opy_ (u"ࠫࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩ௾"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠬࡉࡉࠨ௿"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫఀ") and str(os.getenv(bstack1l_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࠪఁ"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ం"):
    return os.getenv(bstack1l_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠬః"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠪࡇࡎ࠭ఄ"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩఅ") and str(os.getenv(bstack1l_opy_ (u"ࠬࡍࡉࡕࡎࡄࡆࡤࡉࡉࠨఆ"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫఇ"):
    return os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠪఈ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࠫఉ"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧఊ") and str(os.getenv(bstack1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊ࠭ఋ"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩఌ"):
    return os.getenv(bstack1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ఍"), 0)
  if str(os.getenv(bstack1l_opy_ (u"࠭ࡔࡇࡡࡅ࡙ࡎࡒࡄࠨఎ"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬఏ"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨఐ"), 0)
  return -1
def bstack1l111ll_opy_(bstack1l11ll11_opy_):
  global CONFIG
  if not bstack1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ఑") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఒ")]:
    return
  CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ఓ")] = CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧఔ")].replace(
    bstack1l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨక"),
    str(bstack1l11ll11_opy_)
  )
def bstack1lll1ll1_opy_():
  global CONFIG
  if not bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ఖ") in CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪగ")]:
    return
  current_time = datetime.datetime.now()
  bstack1lllllll_opy_ = current_time.strftime(bstack1l_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧఘ"))
  CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఙ")] = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭చ")].replace(
    bstack1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫఛ"),
    bstack1lllllll_opy_
  )
def bstack1111l1l1_opy_():
  global CONFIG
  if bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨజ") in CONFIG and not bool(CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఝ")]):
    del CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪఞ")]
    return
  if not bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫట") in CONFIG:
    CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬఠ")] = bstack1l_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧడ")
  if bstack1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫఢ") in CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨణ")]:
    bstack1lll1ll1_opy_()
    os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫత")] = CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪథ")]
  if not bstack1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫద") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬధ")]:
    return
  bstack1l11ll11_opy_ = bstack1l_opy_ (u"ࠫࠬన")
  bstack11111ll_opy_ = bstack1lll111l_opy_()
  if bstack11111ll_opy_ != -1:
    bstack1l11ll11_opy_ = bstack1l_opy_ (u"ࠬࡉࡉࠡࠩ఩") + str(bstack11111ll_opy_)
  if bstack1l11ll11_opy_ == bstack1l_opy_ (u"࠭ࠧప"):
    bstack1ll11l_opy_ = bstack1l1l11ll_opy_(CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪఫ")])
    if bstack1ll11l_opy_ != -1:
      bstack1l11ll11_opy_ = str(bstack1ll11l_opy_)
  if bstack1l11ll11_opy_:
    bstack1l111ll_opy_(bstack1l11ll11_opy_)
    os.environ[bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬబ")] = CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫభ")]
def bstack11ll1l1_opy_(bstack1ll1l1_opy_, bstack111l1ll1_opy_, path):
  bstack11llll_opy_ = {
    bstack1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧమ"): bstack111l1ll1_opy_
  }
  if os.path.exists(path):
    bstack11l111l_opy_ = json.load(open(path, bstack1l_opy_ (u"ࠫࡷࡨࠧయ")))
  else:
    bstack11l111l_opy_ = {}
  bstack11l111l_opy_[bstack1ll1l1_opy_] = bstack11llll_opy_
  with open(path, bstack1l_opy_ (u"ࠧࡽࠫࠣర")) as outfile:
    json.dump(bstack11l111l_opy_, outfile)
def bstack1l1l11ll_opy_(bstack1ll1l1_opy_):
  bstack1ll1l1_opy_ = str(bstack1ll1l1_opy_)
  bstack111lll_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"࠭ࡾࠨఱ")), bstack1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧల"))
  try:
    if not os.path.exists(bstack111lll_opy_):
      os.makedirs(bstack111lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪళ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩఴ"), bstack1l_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬవ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l_opy_ (u"ࠫࡼ࠭శ")):
        pass
      with open(file_path, bstack1l_opy_ (u"ࠧࡽࠫࠣష")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l_opy_ (u"࠭ࡲࠨస")) as bstack1ll1l111_opy_:
      bstack11111l1_opy_ = json.load(bstack1ll1l111_opy_)
    if bstack1ll1l1_opy_ in bstack11111l1_opy_:
      bstack1ll1l11l_opy_ = bstack11111l1_opy_[bstack1ll1l1_opy_][bstack1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫహ")]
      bstack111l1lll_opy_ = int(bstack1ll1l11l_opy_) + 1
      bstack11ll1l1_opy_(bstack1ll1l1_opy_, bstack111l1lll_opy_, file_path)
      return bstack111l1lll_opy_
    else:
      bstack11ll1l1_opy_(bstack1ll1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll1l1_opy_.format(str(e)))
    return -1
def bstack1l11ll1_opy_(config):
  if bstack1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ఺") in config and config[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ఻")] not in bstack11111_opy_:
    return config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ఼ࠬ")]
  elif bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬఽ") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ా")]
  else:
    return None
def bstack1llll1ll_opy_(config):
  if not bstack1l11ll1_opy_(config) or not bstack1llll111_opy_(config):
    return True
  else:
    return False
def bstack11l1ll1l_opy_(config):
  if bstack111ll1_opy_() < version.parse(bstack1l_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬి")):
    return False
  if bstack111ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ీ")):
    return True
  if bstack1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨు") in config and config[bstack1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩూ")] == False:
    return False
  else:
    return True
def bstack11ll111l_opy_(config, index = 0):
  global bstack1l1l11l_opy_
  bstack11l1111_opy_ = {}
  caps = bstack1l1ll_opy_ + bstack1l1l1_opy_
  if bstack1l1l11l_opy_:
    caps += bstack1ll1l_opy_
  if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ") in config:
    for bstack11l1l11_opy_ in config[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౄ")][index]:
      if bstack11l1l11_opy_ in caps + [bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ౅"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧె")]:
        continue
      bstack11l1111_opy_[bstack11l1l11_opy_] = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪే")][index][bstack11l1l11_opy_]
  for key in config:
    if key in caps + [bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫై")]:
      continue
    bstack11l1111_opy_[key] = config[key]
  bstack11l1111_opy_[bstack1l_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ౉")] = socket.gethostname()
  return bstack11l1111_opy_
def bstack11llll1l_opy_(config):
  global bstack1l1l11l_opy_
  bstack1ll1l11_opy_ = {}
  caps = bstack1l1l1_opy_
  if bstack1l1l11l_opy_:
    caps+= bstack1ll1l_opy_
  for key in caps:
    if key in config:
      bstack1ll1l11_opy_[key] = config[key]
  return bstack1ll1l11_opy_
def bstack1l11lll_opy_(bstack11l1111_opy_, bstack1ll1l11_opy_):
  bstack1ll1l1ll_opy_ = {}
  for key in bstack11l1111_opy_.keys():
    if key in bstack1llll1_opy_:
      bstack1ll1l1ll_opy_[bstack1llll1_opy_[key]] = bstack11l1111_opy_[key]
    else:
      bstack1ll1l1ll_opy_[key] = bstack11l1111_opy_[key]
  for key in bstack1ll1l11_opy_:
    if key in bstack1llll1_opy_:
      bstack1ll1l1ll_opy_[bstack1llll1_opy_[key]] = bstack1ll1l11_opy_[key]
    else:
      bstack1ll1l1ll_opy_[key] = bstack1ll1l11_opy_[key]
  return bstack1ll1l1ll_opy_
def bstack11l1l111_opy_(config, index = 0):
  global bstack1l1l11l_opy_
  caps = {}
  bstack1ll1l11_opy_ = bstack11llll1l_opy_(config)
  bstack11111l11_opy_ = bstack1l1l1_opy_
  bstack11111l11_opy_ += bstack1lllll_opy_
  if bstack1l1l11l_opy_:
    bstack11111l11_opy_ += bstack1ll1l_opy_
  if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ొ") in config:
    if bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩో") in config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౌ")][index]:
      caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ్ࠫ")] = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౎")][index][bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭౏")]
    if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౐") in config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౑")][index]:
      caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ౒")] = str(config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౓")][index][bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౔")])
    bstack111l1ll_opy_ = {}
    for bstack11l11l_opy_ in bstack11111l11_opy_:
      if bstack11l11l_opy_ in config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵౕࠪ")][index]:
        if bstack11l11l_opy_ == bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰౖࠪ"):
          bstack111l1ll_opy_[bstack11l11l_opy_] = str(config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")][index][bstack11l11l_opy_] * 1.0)
        else:
          bstack111l1ll_opy_[bstack11l11l_opy_] = config[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ౘ")][index][bstack11l11l_opy_]
        del(config[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౙ")][index][bstack11l11l_opy_])
    bstack1ll1l11_opy_ = update(bstack1ll1l11_opy_, bstack111l1ll_opy_)
  bstack11l1111_opy_ = bstack11ll111l_opy_(config, index)
  if bstack11l1ll1l_opy_(config):
    bstack11l1111_opy_[bstack1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬౚ")] = True
    caps.update(bstack1ll1l11_opy_)
    caps[bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ౛")] = bstack11l1111_opy_
  else:
    bstack11l1111_opy_[bstack1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ౜")] = False
    caps.update(bstack1l11lll_opy_(bstack11l1111_opy_, bstack1ll1l11_opy_))
    if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ౝ") in caps:
      caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ౞")] = caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ౟")]
      del(caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩౠ")])
    if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ౡ") in caps:
      caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨౢ")] = caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨౣ")]
      del(caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ౤")])
  return caps
def bstack1l1l1111_opy_():
  if bstack111ll1_opy_() <= version.parse(bstack1l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ౥")):
    return bstack11ll_opy_
  return bstack1llll_opy_
def bstack11l1lll1_opy_(options):
  return hasattr(options, bstack1l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ౦"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] += v
      else:
        d[k] = v
  return d
def bstack1l1l11l1_opy_(options, bstack1ll11l1_opy_):
  for bstack1111l1ll_opy_ in bstack1ll11l1_opy_:
    if bstack1111l1ll_opy_ in [bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ౧"), bstack1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ౨")]:
      next
    if bstack1111l1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1111l1ll_opy_]= update(options._experimental_options[bstack1111l1ll_opy_], bstack1ll11l1_opy_[bstack1111l1ll_opy_])
    else:
      options.add_experimental_option(bstack1111l1ll_opy_, bstack1ll11l1_opy_[bstack1111l1ll_opy_])
  if bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ౩") in bstack1ll11l1_opy_:
    for arg in bstack1ll11l1_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ౪")]:
      options.add_argument(arg)
    del(bstack1ll11l1_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭౫")])
  if bstack1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭౬") in bstack1ll11l1_opy_:
    for ext in bstack1ll11l1_opy_[bstack1l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ౭")]:
      options.add_extension(ext)
    del(bstack1ll11l1_opy_[bstack1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ౮")])
def bstack1ll1lll_opy_(options, bstack111lll1_opy_):
  if bstack1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ౯") in bstack111lll1_opy_:
    for bstack1l1111ll_opy_ in bstack111lll1_opy_[bstack1l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ౰")]:
      if bstack1l1111ll_opy_ in options._preferences:
        options._preferences[bstack1l1111ll_opy_] = update(options._preferences[bstack1l1111ll_opy_], bstack111lll1_opy_[bstack1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭౱")][bstack1l1111ll_opy_])
      else:
        options.set_preference(bstack1l1111ll_opy_, bstack111lll1_opy_[bstack1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ౲")][bstack1l1111ll_opy_])
  if bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ౳") in bstack111lll1_opy_:
    for arg in bstack111lll1_opy_[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ౴")]:
      options.add_argument(arg)
def bstack1ll1ll_opy_(options, bstack1111lll_opy_):
  if bstack1l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ౵") in bstack1111lll_opy_:
    options.use_webview(bool(bstack1111lll_opy_[bstack1l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭౶")]))
  bstack1l1l11l1_opy_(options, bstack1111lll_opy_)
def bstack111111l_opy_(options, bstack1lll1lll_opy_):
  for bstack11111l_opy_ in bstack1lll1lll_opy_:
    if bstack11111l_opy_ in [bstack1l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪ౷"), bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ౸")]:
      next
    options.set_capability(bstack11111l_opy_, bstack1lll1lll_opy_[bstack11111l_opy_])
  if bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭౹") in bstack1lll1lll_opy_:
    for arg in bstack1lll1lll_opy_[bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ౺")]:
      options.add_argument(arg)
  if bstack1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ౻") in bstack1lll1lll_opy_:
    options.use_technology_preview(bool(bstack1lll1lll_opy_[bstack1l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨ౼")]))
def bstack1l11ll_opy_(options, bstack1ll11l1l_opy_):
  for bstack11ll1ll_opy_ in bstack1ll11l1l_opy_:
    if bstack11ll1ll_opy_ in [bstack1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ౽"), bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ౾")]:
      next
    options._options[bstack11ll1ll_opy_] = bstack1ll11l1l_opy_[bstack11ll1ll_opy_]
  if bstack1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ౿") in bstack1ll11l1l_opy_:
    for bstack1111ll1_opy_ in bstack1ll11l1l_opy_[bstack1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬಀ")]:
      options.add_additional_option(
          bstack1111ll1_opy_, bstack1ll11l1l_opy_[bstack1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಁ")][bstack1111ll1_opy_])
  if bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨಂ") in bstack1ll11l1l_opy_:
    for arg in bstack1ll11l1l_opy_[bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩಃ")]:
      options.add_argument(arg)
def bstack1l1ll1ll_opy_(options, caps):
  if not hasattr(options, bstack1l_opy_ (u"ࠬࡑࡅ࡚ࠩ಄")):
    return
  if options.KEY == bstack1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫಅ") and options.KEY in caps:
    bstack1l1l11l1_opy_(options, caps[bstack1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬಆ")])
  elif options.KEY == bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ಇ") and options.KEY in caps:
    bstack1ll1lll_opy_(options, caps[bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧಈ")])
  elif options.KEY == bstack1l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫಉ") and options.KEY in caps:
    bstack111111l_opy_(options, caps[bstack1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬಊ")])
  elif options.KEY == bstack1l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ಋ") and options.KEY in caps:
    bstack1ll1ll_opy_(options, caps[bstack1l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಌ")])
  elif options.KEY == bstack1l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭಍") and options.KEY in caps:
    bstack1l11ll_opy_(options, caps[bstack1l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧಎ")])
def bstack11lll1ll_opy_(caps):
  browser = bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩಏ")
  if bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨಐ") in caps:
    browser = caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ಑")]
  elif bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ಒ") in caps:
    browser = caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧಓ")]
  browser = str(browser).lower()
  if browser == bstack1l_opy_ (u"ࠧࡪࡲ࡫ࡳࡳ࡫ࠧಔ") or browser == bstack1l_opy_ (u"ࠨ࡫ࡳࡥࡩ࠭ಕ"):
    browser = bstack1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩಖ")
  if browser == bstack1l_opy_ (u"ࠪࡷࡦࡳࡳࡶࡰࡪࠫಗ"):
    browser = bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫಘ")
  if browser not in [bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬಙ"), bstack1l_opy_ (u"࠭ࡥࡥࡩࡨࠫಚ"), bstack1l_opy_ (u"ࠧࡪࡧࠪಛ"), bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨಜ"), bstack1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪಝ")]:
    return None
  try:
    package = bstack1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࢀ࠲ࡴࡶࡴࡪࡱࡱࡷࠬಞ").format(browser)
    name = bstack1l_opy_ (u"ࠫࡔࡶࡴࡪࡱࡱࡷࠬಟ")
    browser_options = getattr(__import__(package, fromlist=[name]), name)
    options = browser_options()
    if not bstack11l1lll1_opy_(options):
      return None
    for bstack1l111l1l_opy_ in caps.keys():
      options.set_capability(bstack1l111l1l_opy_, caps[bstack1l111l1l_opy_])
    bstack1l1ll1ll_opy_(options, caps)
    return options
  except Exception as e:
    logger.debug(str(e))
    return None
def bstack1l111l1_opy_(options, bstack1l111l_opy_):
  if not bstack11l1lll1_opy_(options):
    return
  for bstack1l111l1l_opy_ in bstack1l111l_opy_.keys():
    if bstack1l111l1l_opy_ in bstack1lllll_opy_:
      next
    options.set_capability(bstack1l111l1l_opy_, bstack1l111l_opy_[bstack1l111l1l_opy_])
  bstack1l1ll1ll_opy_(options, bstack1l111l_opy_)
  if bstack1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫಠ") in options._caps:
    if options._caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಡ")] and options._caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬಢ")].lower() != bstack1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩಣ"):
      del options._caps[bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨತ")]
def bstack1l1111l1_opy_(proxy_config):
  if bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧಥ") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠫࡸࡹ࡬ࡑࡴࡲࡼࡾ࠭ದ")] = proxy_config[bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩಧ")]
    del(proxy_config[bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪನ")])
  if bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ಩") in proxy_config and proxy_config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫಪ")].lower() != bstack1l_opy_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࠩಫ"):
    proxy_config[bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ಬ")] = bstack1l_opy_ (u"ࠫࡲࡧ࡮ࡶࡣ࡯ࠫಭ")
  if bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡅࡺࡺ࡯ࡤࡱࡱࡪ࡮࡭ࡕࡳ࡮ࠪಮ") in proxy_config:
    proxy_config[bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩಯ")] = bstack1l_opy_ (u"ࠧࡱࡣࡦࠫರ")
  return proxy_config
def bstack1l1l1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧಱ") in config:
    return proxy
  config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨಲ")] = bstack1l1111l1_opy_(config[bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩಳ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ಴")])
  return proxy
def bstack1llll11l_opy_(self):
  global CONFIG
  global bstack1111111l_opy_
  if bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨವ") in CONFIG and bstack1l1l1111_opy_().startswith(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࠧಶ")):
    return CONFIG[bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪಷ")]
  elif bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬಸ") in CONFIG and bstack1l1l1111_opy_().startswith(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠫಹ")):
    return CONFIG[bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ಺")]
  else:
    return bstack1111111l_opy_(self)
def bstack11l11l11_opy_():
  if bstack111ll1_opy_() < version.parse(bstack1l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࠪ಻")):
    logger.warning(bstack111lllll_opy_.format(bstack111ll1_opy_()))
    return
  global bstack1111111l_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1111111l_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack1llll11l_opy_
def bstack1l11ll1l_opy_(config):
  if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭಼ࠩ") in config:
    if str(config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪಽ")]).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬಾ"):
      return True
    else:
      return False
  elif bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭ಿ") in os.environ:
    if str(os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧೀ")]).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨು"):
      return True
    else:
      return False
  else:
    return False
def bstack1l11l1_opy_(config):
  if bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨೂ") in config:
    return config[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩೃ")]
  if bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬೄ") in config:
    return config[bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭೅")]
  return {}
def bstack111l111l_opy_(caps):
  global bstack1ll111l1_opy_
  if bstack1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩೆ") in caps:
    caps[bstack1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪೇ")][bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩೈ")] = True
    if bstack1ll111l1_opy_:
      caps[bstack1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ೉")][bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೊ")] = bstack1ll111l1_opy_
  else:
    caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫೋ")] = True
    if bstack1ll111l1_opy_:
      caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೌ")] = bstack1ll111l1_opy_
def bstack1ll1l1l_opy_():
  global CONFIG
  if bstack1l11ll1l_opy_(CONFIG):
    bstack11l11l1_opy_ = bstack1l11l1_opy_(CONFIG)
    bstack11l111l1_opy_(bstack1llll111_opy_(CONFIG), bstack11l11l1_opy_)
def bstack11l111l1_opy_(key, bstack11l11l1_opy_):
  global bstack1l1ll11_opy_
  logger.info(bstack1ll111ll_opy_)
  try:
    bstack1l1ll11_opy_ = Local()
    bstack111llll_opy_ = {bstack1l_opy_ (u"ࠨ࡭ࡨࡽ್ࠬ"): key}
    bstack111llll_opy_.update(bstack11l11l1_opy_)
    logger.debug(bstack11111ll1_opy_.format(str(bstack111llll_opy_)))
    bstack1l1ll11_opy_.start(**bstack111llll_opy_)
    if bstack1l1ll11_opy_.isRunning():
      logger.info(bstack1l1ll1_opy_)
  except Exception as e:
    bstack11l1ll_opy_(bstack1l111ll1_opy_.format(str(e)))
def bstack1l11111l_opy_():
  global bstack1l1ll11_opy_
  if bstack1l1ll11_opy_.isRunning():
    logger.info(bstack1l1l1l11_opy_)
    bstack1l1ll11_opy_.stop()
  bstack1l1ll11_opy_ = None
def bstack11l11ll_opy_():
  logger.info(bstack1ll11111_opy_)
  global bstack1l1ll11_opy_
  if bstack1l1ll11_opy_:
    bstack1l11111l_opy_()
  logger.info(bstack1ll1ll1l_opy_)
def bstack1l11l11l_opy_(self, *args):
  logger.error(bstack111l1l_opy_)
  bstack11l11ll_opy_()
def bstack11l1ll_opy_(err):
  logger.critical(bstack1llllll_opy_.format(str(err)))
  atexit.unregister(bstack11l11ll_opy_)
  sys.exit(1)
def bstack111l11l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack11l11ll_opy_)
  sys.exit(1)
def bstack1lll1l11_opy_():
  global CONFIG
  CONFIG = bstack1llll1l1_opy_()
  CONFIG = bstack1l1lll_opy_(CONFIG)
  CONFIG = bstack11llll11_opy_(CONFIG)
  if bstack1llll1ll_opy_(CONFIG):
    bstack11l1ll_opy_(bstack11lllll_opy_)
  CONFIG[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೎")] = bstack1l11ll1_opy_(CONFIG)
  CONFIG[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭೏")] = bstack1llll111_opy_(CONFIG)
  if bstack1l11111_opy_(CONFIG):
    CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೐")] = bstack1l11111_opy_(CONFIG)
    if not os.getenv(bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨ೑")):
      if os.getenv(bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ೒")):
        CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೓")] = os.getenv(bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ೔"))
      else:
        bstack1111l1l1_opy_()
  bstack1l11l111_opy_()
  bstack1llll11_opy_()
  if bstack1l1l11l_opy_:
    CONFIG[bstack1l_opy_ (u"ࠩࡤࡴࡵ࠭ೕ")] = bstack111l1l1l_opy_(CONFIG)
    logger.info(bstack11l1111l_opy_.format(CONFIG[bstack1l_opy_ (u"ࠪࡥࡵࡶࠧೖ")]))
def bstack1llll11_opy_():
  global CONFIG
  global bstack1l1l11l_opy_
  if bstack1l_opy_ (u"ࠫࡦࡶࡰࠨ೗") in CONFIG:
    bstack1l1l11l_opy_ = True
def bstack111l1l1l_opy_(config):
  bstack1l1ll1l1_opy_ = bstack1l_opy_ (u"ࠬ࠭೘")
  app = config[bstack1l_opy_ (u"࠭ࡡࡱࡲࠪ೙")]
  if isinstance(config[bstack1l_opy_ (u"ࠧࡢࡲࡳࠫ೚")], str):
    if os.path.splitext(app)[1] in bstack1l111_opy_:
      if os.path.exists(app):
        bstack1l1ll1l1_opy_ = bstack11l1llll_opy_(config, app)
      elif bstack11lll111_opy_(app):
        bstack1l1ll1l1_opy_ = app
      else:
        bstack11l1ll_opy_(bstack11l1l1l1_opy_.format(app))
    else:
      if bstack11lll111_opy_(app):
        bstack1l1ll1l1_opy_ = app
      elif os.path.exists(app):
        bstack1l1ll1l1_opy_ = bstack11l1llll_opy_(app)
      else:
        bstack11l1ll_opy_(bstack11l111_opy_)
  else:
    if len(app) > 2:
      bstack11l1ll_opy_(bstack111ll1l_opy_)
    elif len(app) == 2:
      if bstack1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭೛") in app and bstack1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ೜") in app:
        if os.path.exists(app[bstack1l_opy_ (u"ࠪࡴࡦࡺࡨࠨೝ")]):
          bstack1l1ll1l1_opy_ = bstack11l1llll_opy_(config, app[bstack1l_opy_ (u"ࠫࡵࡧࡴࡩࠩೞ")], app[bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ೟")])
        else:
          bstack11l1ll_opy_(bstack11l1l1l1_opy_.format(app))
      else:
        bstack11l1ll_opy_(bstack111ll1l_opy_)
    else:
      for key in app:
        if key in bstack11ll1_opy_:
          if key == bstack1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫೠ"):
            if os.path.exists(app[key]):
              bstack1l1ll1l1_opy_ = bstack11l1llll_opy_(config, app[key])
            else:
              bstack11l1ll_opy_(bstack11l1l1l1_opy_.format(app))
          else:
            bstack1l1ll1l1_opy_ = app[key]
        else:
          bstack11l1ll_opy_(bstack1111lll1_opy_)
  return bstack1l1ll1l1_opy_
def bstack11lll111_opy_(bstack1l1ll1l1_opy_):
  import re
  bstack11lllll1_opy_ = re.compile(bstack1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢೡ"))
  bstack1ll111_opy_ = re.compile(bstack1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧೢ"))
  if bstack1l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨೣ") in bstack1l1ll1l1_opy_ or re.fullmatch(bstack11lllll1_opy_, bstack1l1ll1l1_opy_) or re.fullmatch(bstack1ll111_opy_, bstack1l1ll1l1_opy_):
    return True
  else:
    return False
def bstack11l1llll_opy_(config, path, bstack111l1l11_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l_opy_ (u"ࠪࡶࡧ࠭೤")).read()).hexdigest()
  bstack1l1llll_opy_ = bstack111l11l_opy_(md5_hash)
  bstack1l1ll1l1_opy_ = None
  if bstack1l1llll_opy_:
    logger.info(bstack111l111_opy_.format(bstack1l1llll_opy_, md5_hash))
    return bstack1l1llll_opy_
  bstack1l1ll11l_opy_ = MultipartEncoder(
    fields={
        bstack1l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ೥"): (os.path.basename(path), open(os.path.abspath(path), bstack1l_opy_ (u"ࠬࡸࡢࠨ೦")), bstack1l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ೧")),
        bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ೨"): bstack111l1l11_opy_
    }
  )
  response = requests.post(bstack111l1_opy_, data=bstack1l1ll11l_opy_,
                         headers={bstack1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ೩"): bstack1l1ll11l_opy_.content_type}, auth=(bstack1l11ll1_opy_(config), bstack1llll111_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack1l1ll1l1_opy_ = res[bstack1l_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ೪")]
    logger.info(bstack11ll11ll_opy_.format(bstack1l1ll1l1_opy_))
    bstack1lll1l1l_opy_(md5_hash, bstack1l1ll1l1_opy_)
  except ValueError as err:
    bstack11l1ll_opy_(bstack1l1lll11_opy_.format(str(err)))
  return bstack1l1ll1l1_opy_
def bstack1l11l111_opy_():
  global CONFIG
  global bstack1l1l111_opy_
  bstack11l11111_opy_ = 1
  if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ೫") in CONFIG:
    bstack11l11111_opy_ = CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ೬")]
  bstack1l1lllll_opy_ = 0
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೭") in CONFIG:
    bstack1l1lllll_opy_ = len(CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೮")])
  bstack1l1l111_opy_ = int(bstack11l11111_opy_) * int(bstack1l1lllll_opy_)
def bstack111l11l_opy_(md5_hash):
  bstack11ll11l1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠧࡿࠩ೯")), bstack1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ೰"), bstack1l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪೱ"))
  if os.path.exists(bstack11ll11l1_opy_):
    bstack11111l1l_opy_ = json.load(open(bstack11ll11l1_opy_,bstack1l_opy_ (u"ࠪࡶࡧ࠭ೲ")))
    if md5_hash in bstack11111l1l_opy_:
      bstack1ll1ll11_opy_ = bstack11111l1l_opy_[md5_hash]
      bstack111ll1l1_opy_ = datetime.datetime.now()
      bstack111l11ll_opy_ = datetime.datetime.strptime(bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧೳ")], bstack1l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ೴"))
      if (bstack111ll1l1_opy_ - bstack111l11ll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1ll11_opy_[bstack1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ೵")]):
        return None
      return bstack1ll1ll11_opy_[bstack1l_opy_ (u"ࠧࡪࡦࠪ೶")]
  else:
    return None
def bstack1lll1l1l_opy_(md5_hash, bstack1l1ll1l1_opy_):
  bstack111lll_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪ೷")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ೸"))
  if not os.path.exists(bstack111lll_opy_):
    os.makedirs(bstack111lll_opy_)
  bstack11ll11l1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬ೹")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ೺"), bstack1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭೻"))
  bstack11lll1l_opy_ = {
    bstack1l_opy_ (u"࠭ࡩࡥࠩ೼"): bstack1l1ll1l1_opy_,
    bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ೽"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ೾")),
    bstack1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ೿"): str(__version__)
  }
  if os.path.exists(bstack11ll11l1_opy_):
    bstack11111l1l_opy_ = json.load(open(bstack11ll11l1_opy_,bstack1l_opy_ (u"ࠪࡶࡧ࠭ഀ")))
  else:
    bstack11111l1l_opy_ = {}
  bstack11111l1l_opy_[md5_hash] = bstack11lll1l_opy_
  with open(bstack11ll11l1_opy_, bstack1l_opy_ (u"ࠦࡼ࠱ࠢഁ")) as outfile:
    json.dump(bstack11111l1l_opy_, outfile)
def bstack1l111lll_opy_(self):
  return
def bstack11lll1l1_opy_(self):
  return
def bstack1l111l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack111ll11l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l1l1l_opy_
  global bstack1l1ll111_opy_
  global bstack1l1lll1l_opy_
  global bstack11ll1l_opy_
  global bstack1lll11l1_opy_
  global bstack1111111_opy_
  CONFIG[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧം")] = str(bstack1lll11l1_opy_) + str(__version__)
  command_executor = bstack1l1l1111_opy_()
  logger.debug(bstack1l1l111l_opy_.format(command_executor))
  proxy = bstack1l1l1l1_opy_(CONFIG, proxy)
  bstack11llllll_opy_ = 0 if bstack1l1ll111_opy_ < 0 else bstack1l1ll111_opy_
  if bstack11ll1l_opy_ is True:
    bstack11llllll_opy_ = int(threading.current_thread().getName())
  bstack1l111l_opy_ = bstack11l1l111_opy_(CONFIG, bstack11llllll_opy_)
  logger.debug(bstack11lll11l_opy_.format(str(bstack1l111l_opy_)))
  if bstack1l11ll1l_opy_(CONFIG):
    bstack111l111l_opy_(bstack1l111l_opy_)
  if options:
    bstack1l111l1_opy_(options, bstack1l111l_opy_)
  if desired_capabilities:
    if bstack111ll1_opy_() >= version.parse(bstack1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬഃ")):
      desired_capabilities = {}
    else:
      desired_capabilities.update(bstack1l111l_opy_)
  if not options:
    options = bstack11lll1ll_opy_(bstack1l111l_opy_)
  if (
      not options and not desired_capabilities
  ) or (
      bstack111ll1_opy_() < version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ഄ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l111l_opy_)
  logger.info(bstack1ll1l1l1_opy_)
  if bstack111ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧഅ")):
    bstack1111111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack111ll1_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩആ")):
    bstack1111111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1111111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack11l1l1l_opy_ = self.session_id
  if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഇ") in CONFIG and bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩഈ") in CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഉ")][bstack11llllll_opy_]:
    bstack1l1lll1l_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഊ")][bstack11llllll_opy_][bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬഋ")]
  logger.debug(bstack111lll1l_opy_.format(bstack11l1l1l_opy_))
def bstack1l1111_opy_(self, test):
  global CONFIG
  global bstack11l1l1l_opy_
  global bstack1111ll_opy_
  global bstack1l1lll1l_opy_
  global bstack111ll111_opy_
  if bstack11l1l1l_opy_:
    try:
      data = {}
      bstack111llll1_opy_ = None
      if test:
        bstack111llll1_opy_ = str(test.data)
      if bstack111llll1_opy_ and not bstack1l1lll1l_opy_:
        data[bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഌ")] = bstack111llll1_opy_
      if bstack1111ll_opy_:
        if bstack1111ll_opy_.status == bstack1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ഍"):
          data[bstack1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪഎ")] = bstack1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫഏ")
        elif bstack1111ll_opy_.status == bstack1l_opy_ (u"ࠬࡌࡁࡊࡎࠪഐ"):
          data[bstack1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭഑")] = bstack1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഒ")
          if bstack1111ll_opy_.message:
            data[bstack1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨഓ")] = str(bstack1111ll_opy_.message)
      user = CONFIG[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫഔ")]
      key = CONFIG[bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ക")]
      url = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩഖ").format(user, key, bstack11l1l1l_opy_)
      headers = {
        bstack1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫഗ"): bstack1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩഘ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1l1ll_opy_.format(str(e)))
  bstack111ll111_opy_(self, test)
def bstack11ll11l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1ll1_opy_
  bstack1ll1ll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1111ll_opy_
  bstack1111ll_opy_ = self._test
def bstack1ll11lll_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢങ"), bstack1l_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧച"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࡦ࡬ࡶࠧഛ"), bstack1l_opy_ (u"ࠥ࠲ࠧജ")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l_opy_ (u"ࠦ࠯࠴ࡸ࡮࡮ࠥഝ"))))
  if not files:
    pabot._write(bstack1l_opy_ (u"ࠬ࡝ࡁࡓࡐ࠽ࠤࡓࡵࠠࡰࡷࡷࡴࡺࡺࠠࡧ࡫࡯ࡩࡸࠦࡩ࡯ࠢࠥࠩࡸࠨࠧഞ") % outs_dir, pabot.Color.YELLOW)
    return bstack1l_opy_ (u"ࠨࠢട")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1l1111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦഠ") in options:
    del options[bstack1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧഡ")]
  if ROBOT_VERSION < bstack1l_opy_ (u"ࠤ࠷࠲࠵ࠨഢ"):
    stats = {
      bstack1l_opy_ (u"ࠥࡧࡷ࡯ࡴࡪࡥࡤࡰࠧണ"): {bstack1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥത"): 0, bstack1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧഥ"): 0, bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨദ"): 0},
      bstack1l_opy_ (u"ࠢࡢ࡮࡯ࠦധ"): {bstack1l_opy_ (u"ࠣࡶࡲࡸࡦࡲࠢന"): 0, bstack1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഩ"): 0, bstack1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥപ"): 0},
    }
  else:
    stats = {
      bstack1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࠥഫ"): 0,
      bstack1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧബ"): 0,
      bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨഭ"): 0,
      bstack1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣമ"): 0,
    }
  if pabot_args[bstack1l_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢയ")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣര")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l_opy_ (u"ࠥࡥࡷࡺࡩࡧࡣࡦࡸࡸࠨറ")], pabot_args[bstack1l_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࡩ࡯ࡵࡸࡦ࡫ࡵ࡬ࡥࡧࡵࡷࠧല")]
      )
      outputs += [
        bstack1ll11lll_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l_opy_ (u"ࠧ࠵ࠢള")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l_opy_ (u"ࠨࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸࠨഴ"), bstack1l_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠥࡴ࠰ࡻࡱࡱࠨവ") % index),
        )
      ]
    if bstack1l_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣശ") not in options:
      options[bstack1l_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤഷ")] = bstack1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ࠱ࡼࡲࡲࠢസ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll111_opy_(self, ff_profile_dir):
  global bstack1l11l1l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11l1l1_opy_(self, ff_profile_dir)
def bstack1ll11ll1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll111l1_opy_
  bstack1ll1llll_opy_ = []
  if bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഹ") in CONFIG:
    bstack1ll1llll_opy_ = CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഺ")]
  bstack1l1l1l1l_opy_ = len(suite_group) * len(pabot_args[bstack1l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ഻")] or [(bstack1l_opy_ (u"഼ࠢࠣ"), None)]) * len(bstack1ll1llll_opy_)
  pabot_args[bstack1l_opy_ (u"ࠣࡄࡖࡘࡆࡉࡋࡠࡒࡄࡖࡆࡒࡌࡆࡎࡢࡖ࡚ࡔࠢഽ")] = []
  for q in range(bstack1l1l1l1l_opy_):
    pabot_args[bstack1l_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣാ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦി")],
      pabot_args[bstack1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧീ")],
      argfile,
      pabot_args.get(bstack1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥു")),
      pabot_args[bstack1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤൂ")],
      platform[0],
      bstack1ll111l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢൃ")] or [(bstack1l_opy_ (u"ࠣࠤൄ"), None)]
    for platform in enumerate(bstack1ll1llll_opy_)
  ]
def bstack1ll111l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack111l1l1_opy_=bstack1l_opy_ (u"ࠩࠪ൅")):
  global bstack111ll1ll_opy_
  self.platform_index = platform_index
  self.bstack1l111111_opy_ = bstack111l1l1_opy_
  bstack111ll1ll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll1111_opy_
  if not bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬെ") in item.options:
    item.options[bstack1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭േ")] = []
  for v in item.options[bstack1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧൈ")]:
    if bstack1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ൉") in v:
      item.options[bstack1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩൊ")].remove(v)
  item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪോ")].insert(0, bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫൌ").format(item.platform_index))
  item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩ്ࠬ")].insert(0, bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫൎ").format(item.bstack1l111111_opy_))
  return bstack1lll1111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11111lll_opy_
  command[0] = command[0].replace(bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ൏"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൐"), 1)
  return bstack11111lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l1ll1_opy_(bstack111lll11_opy_):
  global bstack1lll11l1_opy_
  bstack1lll11l1_opy_ = bstack111lll11_opy_
  logger.info(bstack11ll1l11_opy_.format(bstack1lll11l1_opy_.split(bstack1l_opy_ (u"ࠧ࠮ࠩ൑"))[0]))
  global bstack1111111_opy_
  global bstack111ll111_opy_
  global bstack1ll1ll1_opy_
  global bstack1l11l1l1_opy_
  global bstack11111lll_opy_
  global bstack111ll1ll_opy_
  global bstack1lll1111_opy_
  global bstack11ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l11l1_opy_(e, bstack1ll1lll1_opy_)
  Service.start = bstack1l111lll_opy_
  Service.stop = bstack11lll1l1_opy_
  webdriver.Remote.__init__ = bstack111ll11l_opy_
  WebDriver.close = bstack1l111l11_opy_
  if (bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൒") in str(bstack111lll11_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l11l1_opy_(e, bstack11l1ll1_opy_)
    Output.end_test = bstack1l1111_opy_
    TestStatus.__init__ = bstack11ll11l_opy_
    WebDriverCreator._get_ff_profile = bstack1lll111_opy_
    QueueItem.__init__ = bstack1ll111l_opy_
    pabot._create_items = bstack1ll11ll1_opy_
    pabot._run = bstack1l1ll1l_opy_
    pabot._create_command_for_execution = bstack1ll11ll_opy_
    pabot._report_results = bstack1l1111l_opy_
def bstack11l111ll_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ൓") in CONFIG and int(CONFIG[bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪൔ")]) > 1:
    logger.warn(bstack1l11l1l_opy_)
def bstack1l1l1lll_opy_(bstack111ll11_opy_, index):
  bstack1l1l1ll1_opy_(bstack1ll11_opy_)
  exec(open(bstack111ll11_opy_).read())
def bstack11llll1_opy_(arg):
  bstack1l1l1ll1_opy_(bstack1lll11_opy_)
  from _pytest.config import main as bstack1l11l1ll_opy_
  bstack1l11l1ll_opy_(arg)
def bstack111111_opy_():
  logger.info(bstack1l1llll1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪൕ"), help=bstack1l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ൖ"))
  parser.add_argument(bstack1l_opy_ (u"࠭࠭ࡶࠩൗ"), bstack1l_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ൘"), help=bstack1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ൙"))
  parser.add_argument(bstack1l_opy_ (u"ࠩ࠰࡯ࠬ൚"), bstack1l_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩ൛"), help=bstack1l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬ൜"))
  parser.add_argument(bstack1l_opy_ (u"ࠬ࠳ࡦࠨ൝"), bstack1l_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ൞"), help=bstack1l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ൟ"))
  bstack1111l111_opy_ = parser.parse_args()
  try:
    bstack1111ll11_opy_ = bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬൠ")
    if bstack1111l111_opy_.framework:
      bstack1111ll11_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨൡ")
    bstack1l11llll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111ll11_opy_)
    bstack11l1l1_opy_ = open(bstack1l11llll_opy_, bstack1l_opy_ (u"ࠪࡶࠬൢ"))
    bstack1111llll_opy_ = bstack11l1l1_opy_.read()
    bstack11l1l1_opy_.close()
    if bstack1111l111_opy_.username:
      bstack1111llll_opy_ = bstack1111llll_opy_.replace(bstack1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫൣ"), bstack1111l111_opy_.username)
    if bstack1111l111_opy_.key:
      bstack1111llll_opy_ = bstack1111llll_opy_.replace(bstack1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ൤"), bstack1111l111_opy_.key)
    if bstack1111l111_opy_.framework:
      bstack1111llll_opy_ = bstack1111llll_opy_.replace(bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൥"), bstack1111l111_opy_.framework)
    file_name = bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ൦")
    file_path = os.path.abspath(file_name)
    bstack1l1l11_opy_ = open(file_path, bstack1l_opy_ (u"ࠨࡹࠪ൧"))
    bstack1l1l11_opy_.write(bstack1111llll_opy_)
    bstack1l1l11_opy_.close()
    logger.info(bstack11ll111_opy_)
  except Exception as e:
    logger.error(bstack11l1ll11_opy_.format(str(e)))
def bstack111l11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack1lll1l11_opy_()
  logger.debug(bstack11ll1111_opy_.format(str(CONFIG)))
  bstack1111l11_opy_()
  atexit.register(bstack11l11ll_opy_)
  signal.signal(signal.SIGINT, bstack1l11l11l_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l11l_opy_)
def bstack11l11lll_opy_(bstack11ll1ll1_opy_, size):
  bstack11l1l1ll_opy_ = []
  while len(bstack11ll1ll1_opy_) > size:
    bstack11ll1lll_opy_ = bstack11ll1ll1_opy_[:size]
    bstack11l1l1ll_opy_.append(bstack11ll1lll_opy_)
    bstack11ll1ll1_opy_   = bstack11ll1ll1_opy_[size:]
  bstack11l1l1ll_opy_.append(bstack11ll1ll1_opy_)
  return bstack11l1l1ll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1111_opy_)
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ൨")  or sys.argv[1] == bstack1l_opy_ (u"ࠪ࠱ࡻ࠭൩"):
    logger.info(bstack1l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫ൪").format(__version__))
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ൫"):
    bstack111111_opy_()
    return
  args = sys.argv
  bstack111l11_opy_()
  global CONFIG
  global bstack1l1l111_opy_
  global bstack11ll1l_opy_
  global bstack1l1ll111_opy_
  global bstack1ll111l1_opy_
  bstack1ll1111l_opy_ = bstack1l_opy_ (u"࠭ࠧ൬")
  if args[1] == bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൭") or args[1] == bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ൮"):
    bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൯")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൰"):
    bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ൱")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൲"):
    bstack1ll1111l_opy_ = bstack1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ൳")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ൴"):
    bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ൵")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ൶"):
    bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ൷")
    args = args[2:]
  else:
    if not bstack1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ൸") in CONFIG or str(CONFIG[bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ൹")]).lower() in [bstack1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൺ"), bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨൻ")]:
      bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨർ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬൽ")]).lower() == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩൾ"):
      bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪൿ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ඀")]).lower() == bstack1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬඁ"):
      bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ං")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඃ")]).lower() == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ඄"):
      bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඅ")
      args = args[1:]
    else:
      bstack11l1ll_opy_(bstack11l11ll1_opy_)
  global bstack1111111_opy_
  global bstack111ll111_opy_
  global bstack1ll1ll1_opy_
  global bstack1l11l1l1_opy_
  global bstack11111lll_opy_
  global bstack111ll1ll_opy_
  global bstack1lll1111_opy_
  global bstack11ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack111l11l1_opy_(e, bstack1ll1lll1_opy_)
  bstack1111111_opy_ = webdriver.Remote.__init__
  bstack11ll11_opy_ = WebDriver.close
  if (bstack1ll1111l_opy_ in [bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪආ"), bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫඇ"), bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඈ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack111l11l1_opy_(e, bstack11l1ll1_opy_)
    bstack111ll111_opy_ = Output.end_test
    bstack1ll1ll1_opy_ = TestStatus.__init__
    bstack1l11l1l1_opy_ = WebDriverCreator._get_ff_profile
    bstack11111lll_opy_ = pabot._run
    bstack111ll1ll_opy_ = QueueItem.__init__
    bstack1lll1111_opy_ = pabot._create_command_for_execution
  if bstack1ll1111l_opy_ == bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧඉ"):
    bstack1ll1l1l_opy_()
    bstack11l111ll_opy_()
    if bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඊ") in CONFIG:
      bstack11ll1l_opy_ = True
      bstack1111l1_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬඋ")]):
        bstack1111l1_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l1l1lll_opy_, args=(args[0], index)))
      for t in bstack1111l1_opy_:
        t.start()
      for t in bstack1111l1_opy_:
        t.join()
    else:
      bstack1l1l1ll1_opy_(bstack1ll11_opy_)
      exec(open(args[0]).read())
  elif bstack1ll1111l_opy_ == bstack1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඌ") or bstack1ll1111l_opy_ == bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪඍ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l11l1_opy_(e, bstack11l1ll1_opy_)
    bstack1ll1l1l_opy_()
    bstack1l1l1ll1_opy_(bstack11l1l_opy_)
    if bstack1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඎ") in args:
      i = args.index(bstack1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫඏ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1l111_opy_))
    args.insert(0, str(bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬඐ")))
    pabot.main(args)
  elif bstack1ll1111l_opy_ == bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩඑ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l11l1_opy_(e, bstack11l1ll1_opy_)
    for a in args:
      if bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨඒ") in a:
        bstack1l1ll111_opy_ = int(a.split(bstack1l_opy_ (u"ࠪ࠾ࠬඓ"))[1])
      if bstack1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨඔ") in a:
        bstack1ll111l1_opy_ = str(a.split(bstack1l_opy_ (u"ࠬࡀࠧඕ"))[1])
    bstack1l1l1ll1_opy_(bstack11l1l_opy_)
    run_cli(args)
  elif bstack1ll1111l_opy_ == bstack1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ඖ"):
    try:
      from _pytest.config import _prepareconfig
    except Exception as e:
      bstack111l11l1_opy_(e, bstack11l1l11l_opy_)
    bstack1ll1l1l_opy_()
    config = _prepareconfig(args)
    bstack1ll11l11_opy_ = config.args
    bstack11lll1_opy_ = config.invocation_params.args
    bstack11lll1_opy_ = list(bstack11lll1_opy_)
    if bstack1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ඗") in bstack11lll1_opy_:
      i = bstack11lll1_opy_.index(bstack1l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪ඘"))
      bstack11lll1_opy_.pop(i+1)
      bstack11lll1_opy_.pop(i)
    if bstack1l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ඙") in bstack11lll1_opy_:
      i = bstack11lll1_opy_.index(bstack1l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫක"))
      bstack11lll1_opy_.pop(i+1)
      bstack11lll1_opy_.pop(i)
    if bstack1l_opy_ (u"ࠫ࠲ࡴࠧඛ") in bstack11lll1_opy_:
      i = bstack11lll1_opy_.index(bstack1l_opy_ (u"ࠬ࠳࡮ࠨග"))
      bstack11lll1_opy_.pop(i+1)
      bstack11lll1_opy_.pop(i)
    bstack1111l11l_opy_ = []
    for arg in bstack11lll1_opy_:
      if arg not in bstack1ll11l11_opy_ and arg != bstack1l_opy_ (u"࠭࠭ࡴࠩඝ"):
        bstack1111l11l_opy_.append(arg)
    bstack1111l11l_opy_.append(bstack1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩඞ"))
    bstack1111l11l_opy_.append(bstack1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧඟ"))
    bstack1111l1l_opy_ = []
    for spec in bstack1ll11l11_opy_:
      bstack1111ll1l_opy_ = []
      bstack1111ll1l_opy_.append(spec)
      bstack1111ll1l_opy_ += bstack1111l11l_opy_
      bstack1111l1l_opy_.append(bstack1111ll1l_opy_)
    bstack11ll1l_opy_ = True
    bstack1l11lll1_opy_ = 1
    if bstack1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩච") in CONFIG:
      bstack1l11lll1_opy_ = CONFIG[bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪඡ")]
    bstack1l1l1l_opy_ = int(bstack1l11lll1_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧජ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨඣ")]):
      for bstack1111ll1l_opy_ in bstack1111l1l_opy_:
        item = {}
        item[bstack1l_opy_ (u"࠭ࡡࡳࡩࠪඤ")] = bstack1111ll1l_opy_
        item[bstack1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ඥ")] = index
        execution_items.append(item)
    bstack111111l1_opy_ = bstack11l11lll_opy_(execution_items, bstack1l1l1l_opy_)
    for execution_item in bstack111111l1_opy_:
      bstack1111l1_opy_ = []
      for item in execution_item:
        bstack1111l1_opy_.append(threading.Thread(name=str(item[bstack1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧඦ")]),
                                            target=bstack11llll1_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠩࡤࡶ࡬࠭ට")],)))
      for t in bstack1111l1_opy_:
        t.start()
      for t in bstack1111l1_opy_:
        t.join()
  else:
    bstack11l1ll_opy_(bstack11l11ll1_opy_)