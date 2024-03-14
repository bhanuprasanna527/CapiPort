import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


def pie_chart_company_asset_weights(company_asset_weights):
    # Create pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=company_asset_weights["Name"],
                values=company_asset_weights["Allocation"],
                marker=dict(colors=px.colors.qualitative.Light24),
                textposition="inside",
                pull=[0.1] * len(company_asset_weights),
                textinfo="percent+label",
            )
        ]
    )

    fig.update_layout(
        title="Asset Allocation",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        autosize=True,
        width=700,
        height=600,
    )

    fig.update_traces(
        marker=dict(
            colors=[
                "lightseagreen",
                "lightcoral",
                "lightskyblue",
                "lightgreen",
                "lightpink",
                "lightyellow",
                "lightblue",
                "lightgrey",
                "lightgoldenrodyellow",
                "lightcyan",
            ]
        )
    )

    st.plotly_chart(fig)


def plot_annual_returns(annual_portfolio_returns):
    # Plot annual returns using Plotly
    annual_returns_fig = go.Figure(
        data=[
            go.Bar(
                x=annual_portfolio_returns.index.year,
                y=annual_portfolio_returns.values,
                marker_color="skyblue",
                opacity=0.7,
            )
        ]
    )
    annual_returns_fig.update_layout(
        title="Annual Returns of Portfolio",
        xaxis_title="Year",
        yaxis_title="Return",
        xaxis=dict(tickmode="linear"),
        yaxis=dict(tickformat=".2%"),
    )

    st.plotly_chart(annual_returns_fig)


def plot_cummulative_returns(cumulative_returns):
    # Plot cumulative returns using Plotly
    cumulative_returns_fig = go.Figure(
        data=go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns.values,
            mode="lines",
            marker=dict(color="skyblue"),
        )
    )
    cumulative_returns_fig.update_layout(
        title="Cumulative Returns of Portfolio",
        xaxis_title="Date",
        yaxis_title="Value (Rupees)",
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(tickformat=".2f"),
    )

    # Display both plots
    st.plotly_chart(cumulative_returns_fig)
