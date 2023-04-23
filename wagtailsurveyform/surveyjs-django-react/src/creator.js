import {SurveyCreator, SurveyCreatorComponent} from "survey-creator-react";
import React from "react";
import ReactDOM from "react-dom";

import "survey-core/defaultV2.min.css";
import "survey-creator-core/survey-creator-core.min.css";

const defaultCreatorOptions = {
    showLogicTab: false,
    showJSONEditorTab: false,
};

export function edit(
    element,
    {
        json,
        id,
        name,
        autoSaveApiEndpoint,
        creatorOptions = {},
        compact = true,
        hasLicense = false,
        csrfToken = ""
    }
) {
    const creatorOptionsCombined = Object.assign(
        defaultCreatorOptions,
        creatorOptions
    );

    if (autoSaveApiEndpoint) {
        creatorOptionsCombined.isAutoSave = true;
    }

    const creator = new SurveyCreator(creatorOptionsCombined);

    creator.toolbox.forceCompact = compact;

    if (hasLicense) {
        creator.haveCommercialLicense = hasLicense;
    }

    creator.JSON = json;

    if (autoSaveApiEndpoint) {
        creator.saveSurveyFunc = (no, callback) => {
            const xhr = new XMLHttpRequest();
            xhr.open("PUT", autoSaveApiEndpoint);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

            if (csrfToken) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            }

            xhr.onload = function () {
                callback(no, true);
            };
            xhr.send(
                JSON.stringify({
                    id: id,
                    name: name,
                    json: JSON.stringify(creator.JSON),
                })
            );
        };
    }

    ReactDOM.render(
        <React.StrictMode>
            <SurveyCreatorComponent creator={creator}/>
        </React.StrictMode>,
        document.getElementById(element)
    );
}
