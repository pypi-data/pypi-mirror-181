import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';
import { Kernel } from '@jupyterlab/services';
import NotebookUtils from './lib/NotebookUtils';
import { executeRpc } from './lib/RPCUtils';

export const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';

let transformerEnabled: boolean = false;
let transformerNotebookPath: string = "";
let transformerNotebookPathOptions: string[] = [];
let transformerProxyUrl: string = "";
let transformerProxyStatus: string = "";

export interface StatusContent {
    notebook_path: string;
    nb_path_options: string[];
    proxy_url: string;
    proxy_status: string;
}

let statusChangeListeners: ((status: StatusContent) => void)[] = [];
export const addStatusChangeListener = (callback: (status: StatusContent) => void): void => {
    statusChangeListeners.push(callback);
    const current_status: StatusContent = {
        notebook_path: transformerNotebookPath,
        nb_path_options: transformerNotebookPathOptions,
        proxy_url: transformerProxyUrl,
        proxy_status: transformerProxyStatus
    }
    callback(current_status);
}

export const triggerStatusUpdate = async (settings: ISettingRegistry.ISettings) => {
    await retrieveProxyInfo(settings);
}

const issueStatusChange = (): void => {
    const current_status: StatusContent = {
        notebook_path: transformerNotebookPath,
        nb_path_options: transformerNotebookPathOptions,
        proxy_url: transformerProxyUrl,
        proxy_status: transformerProxyStatus
    }
    statusChangeListeners.forEach(callback => {
        callback(current_status);
    });
}

const retrieveProxyInfo = async (settings: ISettingRegistry.ISettings) => {
    try {
        const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
        const proxy_info = await executeRpc(kernel, 'proxy.info');
        kernel.shutdown();
        if(proxy_info.nb_paths) {
            if(! proxy_info.nb_paths.includes(transformerNotebookPath)) {
                console.log("Change notebook path to: " + proxy_info.nb_paths[0]);
                setTransformerNotebookPath(settings, proxy_info.nb_paths[0]);
            }
        }
        if(proxy_info.proxy_url && proxy_info.proxy_url !== transformerProxyUrl) {
            console.log("Change proxy URL to: " + proxy_info.proxy_url);
            setTransformerProxyUrl(settings, proxy_info.proxy_url);
        }
        console.log("Proxy status: " + proxy_info.proxy_status);
        transformerProxyStatus = proxy_info.proxy_status;
        transformerNotebookPathOptions = proxy_info.nb_paths;
        issueStatusChange();
    } catch (e) {
        console.warn("Unable to get settings form kernel!");
        console.warn(e);
    }
}

export const getTransformerEnabled = (): boolean => {
    return transformerEnabled;
};

export const setTransformerEnabled = (settings: ISettingRegistry.ISettings, enabled: boolean) => {
    transformerEnabled = enabled;
    let config : IConfig = {
        enabled: enabled,
        notebookPath: transformerNotebookPath,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerNotebookPath = (): string => {
    return transformerNotebookPath;
};

export const setTransformerNotebookPath = (settings: ISettingRegistry.ISettings, notebookPath: string) => {
    transformerNotebookPath = notebookPath;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookPath: notebookPath,
        proxyUrl: transformerProxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

export const getTransformerProxyUrl = (): string => {
    return transformerProxyUrl;
};

export const setTransformerProxyUrl = (settings: ISettingRegistry.ISettings, proxyUrl: string) => {
    transformerProxyUrl = proxyUrl;
    let config : IConfig = {
        enabled: transformerEnabled,
        notebookPath: transformerNotebookPath,
        proxyUrl: proxyUrl
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

interface IConfig {
    enabled: boolean;
    notebookPath: string;
    proxyUrl: string;
}

const defaultConfig: IConfig = {
    enabled: false,
    notebookPath: "",
    proxyUrl: ""
}

export default {
    id: SETTINGS_ID,
    requires: [ ISettingRegistry ],
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry
    ): void => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(async ([settings]) => {
            try {
                let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
                if(typeof transformerSettings.enabled === 'string') {
                    if(transformerSettings.enabled === 'true') {
                        transformerEnabled = true;
                    } else {
                        transformerEnabled = false;
                    }
                } else if(typeof transformerSettings.enabled === 'boolean') {
                    transformerEnabled = transformerSettings.enabled
                }

                if(typeof transformerSettings.notebookPath === 'string') {
                    transformerNotebookPath = transformerSettings.notebookPath;
                }

                if(typeof transformerSettings.proxyUrl === 'string') {
                    transformerProxyUrl = transformerSettings.proxyUrl;
                } else if(typeof transformerSettings.proxyUrl === 'number') {
                    transformerProxyUrl = transformerSettings.proxyUrl.toString();
                }
                issueStatusChange();
            } catch (error) {
                settingRegistry.set(SETTINGS_ID, TRFANFORMER_CONFIG, defaultConfig as unknown as JSONObject).catch((reason: Error) => {
                    console.error('Failed to set transformer config: ' + reason.message);
                });
            }
            retrieveProxyInfo(settings);
            console.log("Settings when starts up: enabled(" + transformerEnabled + "), NotebookPath(" + transformerNotebookPath + "), ProxyUrl(" + transformerProxyUrl + ")");
        });
    },
} as JupyterFrontEndPlugin<void>;
