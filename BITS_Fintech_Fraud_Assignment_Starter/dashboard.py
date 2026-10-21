"""Polished Streamlit UI for the BITS Fintech Fraud Analytics project.
Requires predictions.csv and metrics.json in the same directory.
Run: python -m streamlit run dashboard.py
"""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Fintech Fraud Analytics", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown(r'''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:#f5f7fb;color:#17233b}
[data-testid="stHeader"]{background:rgba(245,247,251,.9)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101a31,#202d51)}[data-testid="stSidebar"] *{color:#eef3ff}
[data-testid="stSidebar"] hr{border-color:#3b4966}.block-container{padding-top:1.8rem;padding-bottom:3rem;max-width:1500px}
.hero{padding:1.6rem 1.8rem;border-radius:22px;color:white;background:linear-gradient(115deg,#171f3d,#292d63 55%,#635bff);box-shadow:0 14px 34px #292d6320;margin-bottom:1.1rem}
.eyebrow{font-size:.74rem;letter-spacing:.15em;text-transform:uppercase;color:#c8caff;font-weight:700;margin-bottom:.55rem}
.hero h1{font-family:Manrope,sans-serif;font-size:2rem;font-weight:800;line-height:1.15;margin:0 0 .55rem;color:white}.hero p{color:#e0e4ff;margin:0}
.section-head{font-family:Manrope,sans-serif;font-weight:800;font-size:1.18rem;margin:.65rem 0 .15rem;color:#18243a}.section-sub{color:#7b8799;font-size:.88rem;margin-bottom:.7rem}
.metric-card{background:white;border:1px solid #e8edf5;border-radius:17px;padding:1rem 1.1rem;min-height:120px;box-shadow:0 4px 16px #1e2d4b09}
.metric-label{color:#758198;font-size:.82rem;font-weight:600;margin-bottom:.5rem}.metric-value{color:#17233b;font-family:Manrope,sans-serif;font-size:1.65rem;font-weight:800;line-height:1.1}.metric-foot{color:#8a94a6;font-size:.76rem;margin-top:.55rem}
.notice{padding:.8rem 1rem;border-radius:12px;border:1px solid #f1d8a6;background:#fff8e8;color:#78531b;font-size:.88rem}
div[data-testid="stPlotlyChart"]{background:white;border:1px solid #e8edf5;border-radius:16px;padding:.4rem}div[data-testid="stDataFrame"]{border:1px solid #e8edf5;border-radius:12px}
.small-muted{color:#8994a7;font-size:.8rem}.pill{display:inline-block;padding:.25rem .6rem;border-radius:999px;background:#eeedff;color:#4f46e5;font-size:.75rem;font-weight:700}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    file = ROOT / 'predictions.csv'
    if not file.exists(): return pd.DataFrame(), {}
    data = pd.read_csv(file)
    metrics = {}
    try:
        metrics = json.loads((ROOT / 'metrics.json').read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError): pass
    return data, metrics

df, metrics = load_data()
if df.empty:
    st.title('Fintech Fraud Analytics')
    st.error('predictions.csv was not found or contains no data. Put it beside dashboard.py and rerun Streamlit.')
    st.stop()
for col in ['amount','is_fraud','prediction','risk_score','hour','latitude','longitude','distance_km','device_change','international']:
    if col in df: df[col] = pd.to_numeric(df[col], errors='coerce')
if 'transaction_id' not in df: df['transaction_id'] = [f'ROW-{i+1:05d}' for i in range(len(df))]
if 'merchant_category' not in df: df['merchant_category'] = 'Unknown'
if 'amount' not in df: df['amount'] = 0.0
if 'is_fraud' not in df: df['is_fraud'] = 0
if 'risk_score' not in df: df['risk_score'] = df.get('prediction', 0)
df['risk_score'] = df['risk_score'].fillna(0).clip(0,1)
df['is_fraud'] = df['is_fraud'].fillna(0).astype(int)
df['merchant_category'] = df['merchant_category'].fillna('Unknown').astype(str)

with st.sidebar:
    st.markdown('## 🛡️ Fraud Analytics')
    st.caption('TRANSACTION RISK WORKSPACE')
    st.divider()
    page = st.radio('NAVIGATION', ['Overview','Model performance','Transaction explorer','Risk analysis'])
    st.divider()
    threshold = st.slider('High-risk threshold', .05, .95, .40, .05, help='Transactions at or above this score are flagged for review.')
    cats = sorted(df.merchant_category.unique().tolist())
    selected = st.multiselect('Merchant categories', cats, default=cats)
    st.divider()
    st.caption(f'{len(df):,} scored transactions loaded')
    st.caption('Synthetic, rule-generated labels; scores are not proof of fraud.')

view = df[df.merchant_category.isin(selected)].copy()
view['high_risk'] = view.risk_score >= threshold
n = len(view); flagged = view[view.high_risk]; nflag = len(flagged)
flag_share = nflag/n if n else 0
flag_value = float(flagged.amount.sum()) if n else 0

LAYOUT = dict(paper_bgcolor='white',plot_bgcolor='white',font=dict(family='DM Sans',color='#64748b',size=12),margin=dict(l=18,r=18,t=40,b=18),xaxis=dict(showgrid=False,zeroline=False,linecolor='#edf0f6'),yaxis=dict(gridcolor='#edf0f6',zeroline=False))
def figstyle(fig, height=340): fig.update_layout(**LAYOUT,height=height); return fig
def section(title, sub=''):
    st.markdown(f'<div class="section-head">{title}</div>'+ (f'<div class="section-sub">{sub}</div>' if sub else ''), unsafe_allow_html=True)
def card(label,value,foot,icon):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{icon} &nbsp; {label}</div><div class="metric-value">{value}</div><div class="metric-foot">{foot}</div></div>',unsafe_allow_html=True)
def pct(x): return f'{x:.1%}'

st.markdown(f'<div class="hero"><div class="eyebrow">FINANCIAL CRIME · DECISION SUPPORT</div><h1>{page}</h1><p>Explore transaction patterns, review risk signals, and inspect model outputs.</p><div style="margin-top:1rem"><span class="pill">LIVE FILTERS</span> <span style="color:#e0e4ff;font-size:.82rem;margin-left:.45rem">{n:,} transactions in current view</span></div></div>',unsafe_allow_html=True)
st.markdown('<div class="notice">⚠️ <b>Synthetic coursework data:</b> labels are rule-generated. Use these metrics to demonstrate the pipeline, not to claim real-world fraud accuracy.</div>',unsafe_allow_html=True)
st.write('')

if page == 'Overview':
    cols = st.columns(4, gap='medium')
    with cols[0]: card('Transactions reviewed',f'{n:,}','Current filtered test set','↗')
    with cols[1]: card('Flagged high risk',f'{nflag:,}',f'Threshold ≥ {threshold:.2f}','⚑')
    with cols[2]: card('High-risk share',pct(flag_share),'Share of reviewed transactions','◉')
    with cols[3]: card('Value in flagged group',f'{flag_value:,.2f}','Sum of transaction amounts','＄')
    st.write(''); left,right=st.columns([1.15,1],gap='medium')
    with left:
        section('Transactions by merchant','Volume and high-risk flags across categories')
        cat=view.groupby('merchant_category').agg(transactions=('transaction_id','count'),high_risk=('high_risk','sum')).reset_index()
        long=cat.melt(id_vars='merchant_category',value_vars=['transactions','high_risk'],var_name='series',value_name='count')
        f=px.bar(long,x='merchant_category',y='count',color='series',barmode='group',color_discrete_map={'transactions':'#c7d2fe','high_risk':'#635bff'})
        f.update_layout(xaxis_title='',yaxis_title='Transactions',legend_title=''); st.plotly_chart(figstyle(f,360),use_container_width=True)
    with right:
        section('Risk score distribution','The orange line shows the selected review threshold')
        f=px.histogram(view,x='risk_score',nbins=28,color_discrete_sequence=['#635bff'])
        f.add_vline(x=threshold,line_dash='dash',line_color='#f97316',annotation_text=f'{threshold:.2f} threshold',annotation_position='top')
        f.update_layout(xaxis_title='Risk score',yaxis_title='Transactions',bargap=.06); st.plotly_chart(figstyle(f,360),use_container_width=True)
    st.write(''); section('Highest-risk transactions','Prioritized for review · sorted by model risk score')
    cols=[c for c in ['transaction_id','customer_id','amount','merchant_category','hour','risk_score','is_fraud','prediction'] if c in view]
    top=view.sort_values('risk_score',ascending=False).head(10)[cols].copy()
    top['risk_score']=top.risk_score.map(lambda x:f'{x:.3f}')
    st.dataframe(top,use_container_width=True,hide_index=True)
    st.download_button('⬇ Download current filtered data (CSV)',view.to_csv(index=False).encode(),file_name='filtered_fraud_transactions.csv',mime='text/csv')

elif page == 'Model performance':
    section('Model evaluation','Saved metrics from metrics.json plus fraud-class metrics at the selected threshold.')
    y=view.is_fraud.astype(int); pred=(view.risk_score>=threshold).astype(int)
    tp=int(((y==1)&(pred==1)).sum()); tn=int(((y==0)&(pred==0)).sum()); fp=int(((y==0)&(pred==1)).sum()); fn=int(((y==1)&(pred==0)).sum())
    precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0; f1=2*precision*recall/(precision+recall) if precision+recall else 0; accuracy=(tp+tn)/n if n else 0
    cols=st.columns(4,gap='medium')
    with cols[0]: card('Saved accuracy',pct(float(metrics.get('accuracy',accuracy))),'From metrics.json','✓')
    with cols[1]: card('Fraud precision',pct(precision),'TP / (TP + FP)','◎')
    with cols[2]: card('Fraud recall',pct(recall),'TP / (TP + FN)','↗')
    with cols[3]: card('Fraud F1',pct(f1),'Precision/recall balance','✦')
    st.write(''); left,right=st.columns([.85,1.15],gap='medium')
    with left:
        section('Confusion matrix','Actual label vs threshold-based prediction')
        cm=pd.DataFrame([[tn,fp],[fn,tp]],index=['Actual non-fraud','Actual fraud'],columns=['Predicted non-fraud','Predicted fraud'])
        f=px.imshow(cm,text_auto=True,aspect='auto',color_continuous_scale=['#f3f4ff','#635bff']); f.update_layout(coloraxis_showscale=False,xaxis_title='',yaxis_title='')
        st.plotly_chart(figstyle(f,340),use_container_width=True)
    with right:
        section('Classification metrics','Fraud-class values change with the threshold')
        perf=pd.DataFrame({'Metric':['Precision','Recall','F1','Accuracy'],'Value':[precision,recall,f1,accuracy]})
        f=px.bar(perf,x='Metric',y='Value',text=perf.Value.map(lambda v:f'{v:.1%}'),color='Metric',color_discrete_sequence=['#635bff','#8b83ff','#b4adff','#d8d5ff'])
        f.update_traces(textposition='outside',cliponaxis=False); f.update_yaxes(range=[0,1.12],tickformat='.0%'); f.update_layout(showlegend=False,xaxis_title='',yaxis_title='Score')
        st.plotly_chart(figstyle(f,340),use_container_width=True)
    section('Saved pipeline metrics','Original metrics.json content')
    if metrics: st.json(metrics,expanded=True)
    else: st.info('metrics.json not found; computed metrics are shown above.')
    st.caption('The saved ROC-AUC reflects the model evaluation in metrics.json. Binary predictions alone are not sufficient to reconstruct the ROC curve.')

elif page == 'Transaction explorer':
    section('Find a transaction','Search by transaction ID or customer ID and inspect its score.')
    query=st.text_input('Transaction or customer ID',placeholder='e.g. TX0007830 or C002284')
    lo=float(view.amount.min()) if n else 0; hi=float(view.amount.max()) if n else 0
    if lo < hi: ar=st.slider('Transaction amount range',min_value=lo,max_value=hi,value=(lo,hi))
    else: ar=(lo,hi)
    results=view[view.amount.between(ar[0],ar[1])]
    if query.strip():
        mask=results.transaction_id.astype(str).str.contains(query.strip(),case=False,na=False)
        if 'customer_id' in results: mask |= results.customer_id.astype(str).str.contains(query.strip(),case=False,na=False)
        results=results[mask]
    results=results.sort_values('risk_score',ascending=False); st.caption(f'{len(results):,} matching transactions')
    cols=[c for c in ['transaction_id','customer_id','amount','merchant_category','hour','distance_km','device_change','international','risk_score','is_fraud','prediction'] if c in results]
    st.dataframe(results[cols],use_container_width=True,hide_index=True)
    if not results.empty:
        tid=st.selectbox('Inspect a transaction',results.transaction_id.astype(str).tolist()); row=results[results.transaction_id.astype(str)==tid].iloc[0]
        a,b=st.columns([.9,1.1],gap='medium')
        with a:
            g=go.Figure(go.Indicator(mode='gauge+number',value=float(row.risk_score),number={'valueformat':'.3f'},title={'text':'Model risk score'},gauge={'axis':{'range':[0,1]},'bar':{'color':'#635bff'},'steps':[{'range':[0,.25],'color':'#e6f7ef'},{'range':[.25,.6],'color':'#fff1d6'},{'range':[.6,1],'color':'#ffe3e3'}],'threshold':{'line':{'color':'#f97316','width':4},'thickness':.8,'value':threshold}}))
            g.update_layout(paper_bgcolor='white',font={'family':'DM Sans','color':'#334155'},margin=dict(l=20,r=20,t=55,b=10),height=280); st.plotly_chart(g,use_container_width=True)
        with b:
            st.markdown('#### Transaction summary'); st.write(f"**Transaction:** `{row['transaction_id']}`")
            if 'customer_id' in row.index: st.write(f"**Customer:** `{row['customer_id']}`")
            st.write(f"**Amount:** {float(row.amount):,.2f}"); st.write(f"**Merchant category:** {row.merchant_category}")
            st.write(f"**Decision:** {'⚠️ Flag for review' if float(row.risk_score)>=threshold else '✓ Below threshold'}")
            st.info('This score is a prioritization signal, not proof of fraudulent activity.')
    else: st.info('No transactions match those filters.')

else:
    section('Risk patterns','Explore categories and transaction hours. Geographic coordinates are synthetic and should not be interpreted as real locations.')
    left,right=st.columns(2,gap='medium')
    with left:
        section('Risk by merchant category')
        rc=view.groupby('merchant_category').agg(transactions=('transaction_id','count'),flagged=('high_risk','sum'),avg_score=('risk_score','mean'),amount=('amount','sum')).reset_index()
        rc['flag_rate']=rc.flagged/rc.transactions.clip(lower=1)
        f=px.bar(rc.sort_values('flag_rate',ascending=False),x='merchant_category',y='flag_rate',color='avg_score',color_continuous_scale=['#d9d6ff','#635bff'],hover_data=['transactions','flagged','amount'])
        f.update_yaxes(tickformat='.0%'); f.update_layout(xaxis_title='',yaxis_title='Flag rate',coloraxis_colorbar_title='Avg. score'); st.plotly_chart(figstyle(f,360),use_container_width=True)
    with right:
        section('Risk by transaction hour')
        if 'hour' in view:
            h=view.groupby('hour').agg(avg_risk=('risk_score','mean'),flagged=('high_risk','sum')).reset_index().sort_values('hour')
            f=go.Figure(); f.add_trace(go.Scatter(x=h.hour,y=h.avg_risk,mode='lines+markers',line=dict(color='#635bff',width=3),name='Average risk'))
            f.add_trace(go.Bar(x=h.hour,y=h.flagged,name='Flagged transactions',marker_color='#c7d2fe',opacity=.65,yaxis='y2'))
            f.update_layout(yaxis=dict(title='Average risk',tickformat='.0%',range=[0,1]),yaxis2=dict(title='Flagged',overlaying='y',side='right',showgrid=False),xaxis_title='Hour of day',legend=dict(orientation='h',y=1.12))
            st.plotly_chart(figstyle(f,360),use_container_width=True)
        else: st.info('No hour field is available in predictions.csv.')
    section('Flagged transaction register','Transactions above the selected risk threshold')
    risk=view[view.risk_score>=threshold].sort_values('risk_score',ascending=False)
    cols=[c for c in ['transaction_id','customer_id','amount','merchant_category','hour','risk_score'] if c in risk]
    st.dataframe(risk[cols],use_container_width=True,hide_index=True)
    st.download_button('⬇ Export flagged transactions',risk.to_csv(index=False).encode(),file_name='high_risk_transactions.csv',mime='text/csv')

st.write(''); st.markdown('<div class="small-muted">Fintech Fraud Analytics · Coursework prototype · MongoDB + PySpark MLlib + Streamlit</div>',unsafe_allow_html=True)
