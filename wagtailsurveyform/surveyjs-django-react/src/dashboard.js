import React, {Component} from 'react';
import ReactDOM from "react-dom";

import {Model} from 'survey-core';
import {VisualizationPanel} from 'survey-analytics';
import * as SurveyAnalyticsTabulator from "survey-analytics/survey.analytics.tabulator";

import 'survey-analytics/survey.analytics.min.css';
import "tabulator-tables/dist/css/tabulator.min.css";
import "survey-analytics/survey.analytics.tabulator.css";


const defaultVizPanelOptions = {
    allowHideQuestions: false
}

class Dashboard extends Component {

    state = {
        survey: null,
        results: null
    }

    componentDidMount() {
        const {surveyDataUrl} = this.props
        fetch(surveyDataUrl).then(res => res.json()).then(data => {
            const {survey, results} = data
            this.setState({survey: new Model(survey.json), results: results.map(r => r.form_data)})
        })
    }

    renderVizPanel = () => {

        const {tabular, vizPanelOptions, element} = this.props

        const vizPanelOptionsCombined = Object.assign(defaultVizPanelOptions, vizPanelOptions)


        const {survey, results} = this.state

        if (survey && results && this.panel) {

            if (tabular) {
                const vizPanel = new SurveyAnalyticsTabulator.Tabulator(
                    survey,
                    results,
                    vizPanelOptionsCombined
                );
                vizPanel.showHeader = false;
                vizPanel.render(this.panel);

            } else {
                const vizPanel = new VisualizationPanel(
                    survey.getAllQuestions(),
                    results,
                    vizPanelOptionsCombined
                );
                vizPanel.showHeader = true;
                vizPanel.render(this.panel);
            }
        }

        return null
    }

    render() {
        return <div className="vizpanel-render" ref={(input) => {
            this.panel = input;
        }}> {this.renderVizPanel()}</div>
    }
}


export function dashboard(
    element,
    {
        surveyDataUrl,
        tabular = false,
        vizPanelOptions = {}
    }
) {
    ReactDOM.render(
        <React.StrictMode>
            <Dashboard surveyDataUrl={surveyDataUrl} tabular={tabular} vizPanelOptions={vizPanelOptions}
                       container={element}/>
        </React.StrictMode>,
        document.getElementById(element)
    );
}