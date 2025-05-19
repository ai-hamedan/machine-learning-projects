import reflex as rx
from ..components.card import card
from ..templates import template

import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from io import BytesIO
import base64


class State(rx.State):
    show_preview: bool = False

    def toggle_preview(self):
        self.show_preview = not self.show_preview


def confusion_matrix_grid(tp=50, fn=10, fp=5, tn=100):
    def cell(content, **kwargs):
        return rx.box(
            rx.text(content, font_size="14px"),
            display="flex",
            align_items="center",
            justify_content="center",
            padding="8px",
            border="1px solid gray",
            **kwargs
        )
    return rx.vstack(
        rx.heading("Confusion Matrix", size="4"),
        rx.grid(
            # First row: top labels
            rx.box(),  # Empty top-left cell
            rx.text("Predicted: Positive", font_size="12px"),
            rx.text("Predicted: Negative", font_size="12px"),

            # Second row: Actual: Positive
            rx.text("Actual: Positive", font_size="12px"),
            cell(f"{tp}", bg="green.100", border_right=True, border_bottom=True),
            cell(f"{fn}", bg="red.100", border_bottom=True),

            # Third row: Actual: Negative
            rx.text("Actual: Negative", font_size="12px"),
            cell(f"{fp}", bg="orange.100", border_right=True),
            cell(f"{tn}", bg="blue.100"),

            columns="repeat(3, 1fr)",
            gap="0",
            padding="16px",
            width="400px",
        )
    )


def generate_roc_plot():
    X, y = make_classification(n_samples=1000, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_scores = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_scores)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash'), name='Random'))
    fig.update_layout(
        title='ROC Curve',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        margin=dict(l=30, r=30, t=30, b=30),
    )
    return fig

@template(route="/about", title="About")
def about() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            card(
                rx.vstack(
                    rx.heading("Welcome, John Doe", size="5"),
                    rx.heading("Welcome, John Doe", size="5"),                
                )
            ),
            card(
                rx.vstack(
                    rx.heading("Welcome, John Doe", size="5"),
                    rx.heading("Welcome, John Doe", size="5"),                
                )
            ),
            card(
                rx.vstack(
                    rx.heading("Welcome, John Doe", size="5"),
                    rx.heading("Welcome, John Doe", size="5"),                
                )
            ),
            card(
                rx.vstack(
                    rx.heading("Welcome, John Doe", size="5"),
                    rx.heading("Welcome, John Doe", size="5"),                
                )
            ),
            spacing="4",
            width="100%",
        ),
        rx.hstack( 
            card(
                rx.vstack(
                    # rx.heading("Confusion Matrix", size="5"),
                    confusion_matrix_grid()
                )
            ),
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.card(
                        # rx.box(
                            rx.plotly(
                                data=generate_roc_plot(),
                                   width="100%",
                                   height="100%",        
                                   config={"displayModeBar": False}
                            ),                        
                            cursor="zoom-in",
                            on_double_click=State.toggle_preview,
                            width="400px",
                            height="300px",
                    )
                ),
                rx.dialog.content(
                    rx.center(
                        rx.box(
                            rx.plotly(
                                data=generate_roc_plot(),
                                width="100%",
                                height="100%",
                            ),
                            width="50vw",  # 50% of viewport width
                            height="50vh",  # 50% of viewport height
                            background_color="white",
                            border_radius="1em",
                            box_shadow="lg",
                            padding="1em",
                        ),
                        width="100%",
                        height="100%",
                    ),
                ),
                open=State.show_preview,
                on_open_change=lambda open: State.set_show_preview(open)
            )
        )
    )
   