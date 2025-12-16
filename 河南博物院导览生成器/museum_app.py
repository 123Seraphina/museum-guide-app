import streamlit as st
import base64
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO, StringIO
# 页面基础配置
st.set_page_config(
    page_title="河南博物院AI导览系统",
    page_icon="🏛️",
    layout="wide"
)

# ===================== 核心工具函数 =====================
def generate_map_image(route, floor_mode, floor_routes):
    """生成路径地图，支持单层/多楼层联合展示"""
    if floor_mode == "单层":
        # 单层地图渲染逻辑
        floor = list(floor_routes.keys())[0]
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.set_xlim(0, 600)
        ax.set_ylim(0, 400)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.patch.set_facecolor("#f0f2f6")
        # 绘制墙体
        ax.add_patch(patches.Rectangle((0, 0), 600, 400, linewidth=2, edgecolor="#333", facecolor="#fff"))
        
        if floor == "1楼":
            # 1楼展厅结构
            ax.add_patch(patches.Rectangle((50, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="1号展厅"))
            ax.add_patch(patches.Rectangle((250, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="3号展厅"))
            ax.add_patch(patches.Rectangle((450, 50), 100, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="5号展厅"))
            ax.add_patch(patches.Rectangle((250, 0), 200, 50, linewidth=1, edgecolor="#ccc", facecolor="#faf0f5", label="文创商店"))
            pos_map = {
                "AI智能语音导览": (150, 200),
                "AR文物复原体验": (350, 200),
                "AI拍照识文物": (500, 200),
                "AI文创智能推荐": (350, 25)
            }
            ax.text(300, 380, "河南博物院1楼展厅AI服务路径图", ha="center", va="center", fontsize=12, weight="bold")
        else:
            # 2楼展厅结构
            ax.add_patch(patches.Rectangle((50, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="2号展厅"))
            ax.add_patch(patches.Rectangle((250, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="4号展厅"))
            ax.add_patch(patches.Rectangle((450, 50), 100, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="6号展厅"))
            ax.add_patch(patches.Rectangle((250, 0), 200, 50, linewidth=1, edgecolor="#ccc", facecolor="#faf0f5", label="学术报告厅"))
            pos_map = {
                "AI智能语音导览": (150, 200),
                "AR文物复原体验": (350, 200),
                "AI拍照识文物": (500, 200),
                "AI虚拟历史对话": (350, 25)
            }
            ax.text(300, 380, "河南博物院2楼展厅AI服务路径图", ha="center", va="center", fontsize=12, weight="bold")
        
        # 颜色映射
        color_map = {
            "AI智能语音导览": "red",
            "AR文物复原体验": "blue",
            "AI拍照识文物": "green",
            "AI文创智能推荐": "purple",
            "AI虚拟历史对话": "orange"
        }
        # 绘制点位和动线
        x_coords, y_coords = [], []
        for service in route:
            x, y = pos_map[service]
            x_coords.append(x)
            y_coords.append(y)
            ax.scatter(x, y, color=color_map[service], s=150, zorder=3)
            ax.text(x, y + 20, service.replace("AI", "").replace("体验", ""), 
                    ha="center", va="bottom", fontsize=8, weight="bold")
        if len(x_coords) > 1:
            ax.plot(x_coords, y_coords, color="#ff9900", linewidth=2, linestyle="--", zorder=2)
        plt.legend(loc="upper right", fontsize=8)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return Image.open(buf)
    else:
        # 多楼层联合地图：左右分栏展示1、2楼路径
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=100)
        for ax, floor in zip([ax1, ax2], ["1楼", "2楼"]):
            ax.set_xlim(0, 600)
            ax.set_ylim(0, 400)
            ax.set_aspect("equal")
            ax.axis("off")
            ax.add_patch(patches.Rectangle((0, 0), 600, 400, linewidth=2, edgecolor="#333", facecolor="#fff"))
            
            if floor == "1楼":
                ax.add_patch(patches.Rectangle((50, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="1号展厅"))
                ax.add_patch(patches.Rectangle((250, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="3号展厅"))
                ax.add_patch(patches.Rectangle((450, 50), 100, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="5号展厅"))
                ax.add_patch(patches.Rectangle((250, 0), 200, 50, linewidth=1, edgecolor="#ccc", facecolor="#faf0f5", label="文创商店"))
                pos_map = {
                    "AI智能语音导览": (150, 200),
                    "AR文物复原体验": (350, 200),
                    "AI拍照识文物": (500, 200),
                    "AI文创智能推荐": (350, 25)
                }
                ax.text(300, 380, "1楼展厅路径", ha="center", va="center", fontsize=12, weight="bold")
                route = floor_routes["1楼"]
            else:
                ax.add_patch(patches.Rectangle((50, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="2号展厅"))
                ax.add_patch(patches.Rectangle((250, 50), 200, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="4号展厅"))
                ax.add_patch(patches.Rectangle((450, 50), 100, 300, linewidth=1, edgecolor="#ccc", facecolor="#f8f9fa", label="6号展厅"))
                ax.add_patch(patches.Rectangle((250, 0), 200, 50, linewidth=1, edgecolor="#ccc", facecolor="#faf0f5", label="学术报告厅"))
                pos_map = {
                    "AI智能语音导览": (150, 200),
                    "AR文物复原体验": (350, 200),
                    "AI拍照识文物": (500, 200),
                    "AI虚拟历史对话": (350, 25)
                }
                ax.text(300, 380, "2楼展厅路径", ha="center", va="center", fontsize=12, weight="bold")
                route = floor_routes["2楼"]
            
            color_map = {
                "AI智能语音导览": "red",
                "AR文物复原体验": "blue",
                "AI拍照识文物": "green",
                "AI文创智能推荐": "purple",
                "AI虚拟历史对话": "orange"
            }
            x_coords, y_coords = [], []
            for service in route:
                x, y = pos_map[service]
                x_coords.append(x)
                y_coords.append(y)
                ax.scatter(x, y, color=color_map[service], s=150, zorder=3)
                ax.text(x, y + 20, service.replace("AI", "").replace("体验", ""), 
                        ha="center", va="bottom", fontsize=8, weight="bold")
            if len(x_coords) > 1:
                ax.plot(x_coords, y_coords, color="#ff9900", linewidth=2, linestyle="--", zorder=2)
            ax.legend(loc="upper right", fontsize=8)
        
        fig.suptitle("河南博物院跨楼层AI服务完整游览路径图", fontsize=14, weight="bold", y=0.98)
        fig.patch.set_facecolor("#f0f2f6")
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return Image.open(buf)

def get_route_detail(route, floor, floor_mode="单层", custom_note="", floor_routes=None):
    """生成路径详情，支持多楼层汇总与个性化备注"""
    if floor_mode == "单层":
        if floor == "1楼":
            detail_map = {
                "AI智能语音导览": {"pos": "1号展厅入口（1楼）", "dist": "0米", "desc": "智能讲解青铜器、妇好鸮尊等核心文物，支持语音问答"},
                "AR文物复原体验": {"pos": "3号展厅中央（1楼）", "dist": "200米", "desc": "手机AR还原文物铸造场景，沉浸式感受商周青铜文明"},
                "AI拍照识文物": {"pos": "5号展厅出口（1楼）", "dist": "350米", "desc": "拍照即可识别文物，自动推送深度历史背景与学术资料"},
                "AI文创智能推荐": {"pos": "文创商店内（1楼）", "dist": "500米", "desc": "根据喜爱文物定制专属文创，支持线上预订"}
            }
        else:
            detail_map = {
                "AI智能语音导览": {"pos": "2号展厅入口（2楼）", "dist": "0米", "desc": "智能讲解陶瓷器、贾湖骨笛等核心文物，支持语音问答"},
                "AR文物复原体验": {"pos": "4号展厅中央（2楼）", "dist": "200米", "desc": "手机AR还原文物烧制场景，沉浸式感受汉唐陶瓷文明"},
                "AI拍照识文物": {"pos": "6号展厅出口（2楼）", "dist": "350米", "desc": "拍照即可识别文物，自动推送深度历史背景与学术资料"},
                "AI虚拟历史对话": {"pos": "学术报告厅旁（2楼）", "dist": "500米", "desc": "与虚拟历史人物实时互动，解答文物相关历史疑问"}
            }
        total_dist = 0
        detail_text = f"### {floor}路径详情\n"
        for idx, service in enumerate(route, 1):
            info = detail_map[service]
            total_dist = int(info["dist"])
            detail_text += f"""
**第{idx}站：{service}**
- 📍 位置：{info["pos"]}
- 🚶 累计步行：{total_dist}米
- 💡 服务说明：{info["desc"]}
            """
        detail_text += f"\n⏰ {floor}预计游览时长：{len(route)*0.5}小时\n"
        # 新增个性化备注
        if custom_note:
            detail_text += f"\n📝 **个性化备注**：{custom_note}\n"
        return detail_text
    else:
        # 多楼层详情汇总
        detail_text = "### 跨楼层完整路径详情\n"
        total_time = 0
        total_walk = 0
        for floor, route in floor_routes.items():
            if floor == "1楼":
                detail_map = {
                    "AI智能语音导览": {"pos": "1号展厅入口（1楼）", "dist": "0米", "desc": "智能讲解青铜器、妇好鸮尊等核心文物"},
                    "AR文物复原体验": {"pos": "3号展厅中央（1楼）", "dist": "200米", "desc": "AR还原青铜铸造场景"},
                    "AI拍照识文物": {"pos": "5号展厅出口（1楼）", "dist": "350米", "desc": "拍照识文物并推送资料"},
                    "AI文创智能推荐": {"pos": "文创商店（1楼）", "dist": "500米", "desc": "定制专属文创"}
                }
            else:
                detail_map = {
                    "AI智能语音导览": {"pos": "2号展厅入口（2楼）", "dist": "0米", "desc": "智能讲解陶瓷器、贾湖骨笛等文物"},
                    "AR文物复原体验": {"pos": "4号展厅中央（2楼）", "dist": "200米", "desc": "AR还原陶瓷烧制场景"},
                    "AI拍照识文物": {"pos": "6号展厅出口（2楼）", "dist": "350米", "desc": "拍照识文物并推送资料"},
                    "AI虚拟历史对话": {"pos": "学术报告厅旁（2楼）", "dist": "500米", "desc": "与虚拟历史人物互动"}
                }
            detail_text += f"\n**【{floor}】**\n"
            floor_walk = 0
            for idx, service in enumerate(route, 1):
                info = detail_map[service]
                floor_walk = int(info["dist"])
                detail_text += f"{idx}. **{service}** - {info['pos']}（步行{info['dist']}米）\n"
            total_walk += floor_walk
            floor_time = len(route)*0.5
            total_time += floor_time
            detail_text += f"{floor}预计时长：{floor_time}小时\n"
        
        detail_text += f"\n📊 整体统计：\n- 累计步行：{total_walk + 50}米（含楼层间换乘50米）\n- 总预计游览时长：{total_time + 0.2}小时（含换乘时间）"
        # 新增个性化备注
        if custom_note:
            detail_text += f"\n\n📝 **个性化备注**：{custom_note}"
        return detail_text

# ===================== 全局路径规则 =====================
def get_cross_floor_routes(age, ai_service_1f, ai_service_2f):
    """生成跨楼层路径规则"""
    route_1f_rules = {
        "18岁及以下": ["AI智能语音导览", "AR文物复原体验"],
        "18-25岁": ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI文创智能推荐"],
        "26-35岁": ["AI智能语音导览", "AI拍照识文物", "AR文物复原体验"],
        "36岁以上": ["AI智能语音导览", "AI拍照识文物"]
    }
    route_2f_rules = {
        "18岁及以下": ["AI智能语音导览", "AR文物复原体验"],
        "18-25岁": ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI虚拟历史对话"],
        "26-35岁": ["AI智能语音导览", "AI拍照识文物", "AR文物复原体验"],
        "36岁以上": ["AI智能语音导览", "AI拍照识文物"]
    }
    # 优先按年龄匹配，再按选择的服务微调
    route_1f = route_1f_rules[age]
    if ai_service_1f not in route_1f:
        route_1f.insert(1, ai_service_1f)
    route_2f = route_2f_rules[age]
    if ai_service_2f not in route_2f:
        route_2f.insert(1, ai_service_2f)
    return {"1楼": route_1f, "2楼": route_2f}

# ===================== 页面主体 =====================
st.title("🏛️ 河南博物院AI智慧导览路径生成器")
st.divider()

# 新增路径模式选择
route_mode = st.radio(
    "路径规划模式",
    ["单层展厅路径", "跨楼层完整路径"],
    horizontal=True,
    help="选择生成单层或跨1、2楼的完整游览路径"
)

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("📋 参观信息填写")
    age = st.selectbox(
        "年龄阶段",
        ["18岁及以下", "18-25岁", "26-35岁", "36岁以上"],
        index=1,
        help="不同年龄段匹配不同游览节奏"
    )
    purpose = st.selectbox(
        "参观核心目的",
        ["学习历史知识", "休闲打卡", "亲子教育", "专业研究"],
        index=0
    )
    companion = st.selectbox(
        "同行人群",
        ["朋友/同学", "家人/孩子", "独自一人", "旅行团"],
        index=0
    )

    if route_mode == "单层展厅路径":
        floor = st.selectbox("展厅楼层", ["1楼", "2楼"], index=0)
        if floor == "1楼":
            ai_service = st.selectbox("1楼最想体验的AI服务", 
                                     ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI文创智能推荐"], index=1)
        else:
            ai_service = st.selectbox("2楼最想体验的AI服务", 
                                     ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI虚拟历史对话"], index=1)
    else:
        st.caption("请分别选择1、2楼优先体验的AI服务")
        ai_service_1f = st.selectbox("1楼优先服务", 
                                    ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI文创智能推荐"], index=1)
        ai_service_2f = st.selectbox("2楼优先服务", 
                                    ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI虚拟历史对话"], index=1)
    
    # 新增个性化备注输入框
    st.subheader("✏️ 个性化备注")
    custom_note = st.text_area(
        "填写你的游览重点/特殊需求（如“在妇好鸮尊处多停留”“需要文创商店折扣信息”）",
        placeholder="输入个性化备注，将同步到路径清单中...",
        height=80
    )
    
    generate_btn = st.button("🚀 生成专属路径", type="primary", use_container_width=True)

with col2:
    st.subheader("🗺️ 个性化游览方案")
    if generate_btn:
        if route_mode == "单层展厅路径":
            # 单层路径逻辑
            if floor == "1楼":
                route_rules = {
                    "18岁及以下+AR文物复原体验": ["AI智能语音导览", "AR文物复原体验"],
                    "18-25岁+AR文物复原体验": ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI文创智能推荐"],
                    "18-25岁+AI文创智能推荐": ["AI智能语音导览", "AI文创智能推荐", "AR文物复原体验"],
                    "26-35岁+AI智能语音导览": ["AI智能语音导览", "AI拍照识文物", "AR文物复原体验"],
                    "36岁以上+AI智能语音导览": ["AI智能语音导览", "AI拍照识文物"],
                    "默认": ["AI智能语音导览", "AR文物复原体验"]
                }
            else:
                route_rules = {
                    "18岁及以下+AR文物复原体验": ["AI智能语音导览", "AR文物复原体验"],
                    "18-25岁+AR文物复原体验": ["AI智能语音导览", "AR文物复原体验", "AI拍照识文物", "AI虚拟历史对话"],
                    "18-25岁+AI虚拟历史对话": ["AI智能语音导览", "AI虚拟历史对话", "AR文物复原体验"],
                    "26-35岁+AI智能语音导览": ["AI智能语音导览", "AI拍照识文物", "AR文物复原体验"],
                    "36岁以上+AI智能语音导览": ["AI智能语音导览", "AI拍照识文物"],
                    "默认": ["AI智能语音导览", "AR文物复原体验"]
                }
            current_route = route_rules.get(f"{age}+{ai_service}", route_rules["默认"])
            map_img = generate_map_image(current_route, "单层", {floor: current_route})
            st.image(map_img, caption=f"{floor}AI服务路径可视化地图", use_column_width=True)
            st.divider()
            st.markdown(get_route_detail(current_route, floor, "单层", custom_note))
            # 单层路径下载
            route_text = get_route_detail(current_route, floor, "单层", custom_note).replace("**", "").replace("#", "")
            st.download_button(
                "📥 下载单层路径清单",
                data=route_text,
                file_name=f"河南博物院{floor}AI导览路径.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            # 跨楼层路径逻辑
            floor_routes = get_cross_floor_routes(age, ai_service_1f, ai_service_2f)
            map_img = generate_map_image([], "跨楼层", floor_routes)
            st.image(map_img, caption="跨1、2楼完整游览路径图", use_column_width=True)
            st.divider()
            st.markdown(get_route_detail([], "", "跨楼层", custom_note, floor_routes))
            # 跨楼层路径下载
            cross_route_text = get_route_detail([], "", "跨楼层", custom_note, floor_routes).replace("**", "").replace("#", "")
            st.download_button(
                "📥 下载跨楼层路径清单",
                data=cross_route_text,
                file_name="河南博物院跨楼层AI导览路径.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("请在左侧填写参观信息，点击生成按钮获取专属路径", icon="💡")

# 底部说明
st.divider()
st.caption("数据来源：基于532份河南博物院游客调研数据生成 | 地图为简易示意图，仅供演示")
