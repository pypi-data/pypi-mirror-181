import { JupyterFrontEnd, JupyterFrontEndPlugin, ILayoutRestorer, ILabShell } from '@jupyterlab/application';
import { IToolbarWidgetRegistry, ReactWidget } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { TransformerLeftPanel } from './widgets/TransformerLeftPanel';
import * as React from 'react';
import '../style/index.css';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { SETTINGS_ID } from './settings';

let transformerSettings: ISettingRegistry.ISettings;
export default {
    id: 'modeldeploy-proxy-labextension:leftpanel',
    requires: [ILabShell, ISettingRegistry, ILayoutRestorer, IToolbarWidgetRegistry],
    optional: [ITranslator],
    autoStart: true,
    activate: async (
        app: JupyterFrontEnd,
        labShell: ILabShell,
        settingRegistry: ISettingRegistry,
        restorer: ILayoutRestorer,
        toolbarRegistry: IToolbarWidgetRegistry,
        translator: ITranslator,
    ) => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(([settings]) => {
            transformerSettings = settings;
        });
        let widget: ReactWidget;
        async function loadPanel() {
            if (! widget.isAttached) {
                labShell.add(widget, 'left');
            }
        }

        app.started.then(() => {
            widget = ReactWidget.create(
                <TransformerLeftPanel
                  transformerSettings={transformerSettings}
                />,
            );
            widget.id = 'modeldeploy-proxy-labextension/transformer-leftpanel-widget';
            widget.title.iconClass = 'transformer-logo jp-sidebar-tabicon-transformer';
            widget.title.caption = 'Transformer Panel';
            widget.node.classList.add('transformer-panel');
            restorer.add(widget, widget.id);
        });

        app.restored.then(() => {
            loadPanel();
        });
    },
} as JupyterFrontEndPlugin<void>;
