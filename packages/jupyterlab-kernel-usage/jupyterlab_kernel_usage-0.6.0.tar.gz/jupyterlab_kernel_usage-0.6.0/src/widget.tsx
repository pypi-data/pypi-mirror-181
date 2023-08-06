import React, { useState, useEffect } from 'react';
import { ISignal } from '@lumino/signaling';
import { ReactWidget, ISessionContext } from '@jupyterlab/apputils';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { Kernel } from '@jupyterlab/services';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { requestAPI } from './handler';
import { KernelUsagePanel } from './panel';
import useInterval from './useInterval';
import { formatForDisplay } from './format';

type Usage = {
  timestamp: Date | null;
  kernelId: string;
  hostname: string;
  kernel_cpu: number;
  kernel_memory: number;
  pid: number;
  host_cpu_percent: number;
  cpu_count: number;
  host_virtual_memory: {
    active: number;
    available: number;
    free: number;
    inactive: number;
    percent: number;
    total: number;
    used: number;
    wired: number;
  };
};

const POLL_INTERVAL_SEC = 5;

type KernelChangeCallback = (
  _sender: ISessionContext,
  args: IChangedArgs<
    Kernel.IKernelConnection | null,
    Kernel.IKernelConnection | null,
    'kernel'
  >
) => void;
let kernelChangeCallback: {
  callback: KernelChangeCallback;
  panel: NotebookPanel;
} | null = null;

const KernelUsage = (props: {
  widgetAdded: ISignal<INotebookTracker, NotebookPanel | null>;
  currentNotebookChanged: ISignal<INotebookTracker, NotebookPanel | null>;
  panel: KernelUsagePanel;
}) => {
  const { panel } = props;
  const [kernelId, setKernelId] = useState<string>();
  const [path, setPath] = useState<string>();
  const [usage, setUsage] = useState<Usage | undefined>();

  useInterval(async () => {
    if (kernelId && panel.isVisible) {
      requestUsage(kernelId)
        .then(usage => setUsage(usage))
        .catch(() => {
          console.warn(`Request failed for ${kernelId}. Kernel restarting?`);
        });
    }
  }, POLL_INTERVAL_SEC * 1000);

  const requestUsage = (kid: string) => {
    return requestAPI<any>(`get_usage/${kid}`).then(data => {
      const usage: Usage = {
        ...data.content,
        kernelId: kid,
        timestamp: new Date()
      };
      return usage;
    });
  };

  useEffect(() => {
    const createKernelChangeCallback = (panel: NotebookPanel) => {
      return (
        _sender: ISessionContext,
        args: IChangedArgs<
          Kernel.IKernelConnection | null,
          Kernel.IKernelConnection | null,
          'kernel'
        >
      ) => {
        const newKernelId = args.newValue?.id;
        if (newKernelId) {
          setKernelId(newKernelId);
          const path = panel?.sessionContext.session?.model.path;
          setPath(path);
          requestUsage(newKernelId).then(usage => setUsage(usage));
        } else {
          // Kernel was disposed
          setKernelId(newKernelId);
        }
      };
    };

    const notebookChangeCallback = (
      sender: INotebookTracker,
      panel: NotebookPanel | null
    ) => {
      if (panel === null) {
        // Ideally we would switch to a new "select a notebook to get kernel
        // usage" screen instead of showing outdated info.
        return;
      }
      if (kernelChangeCallback) {
        kernelChangeCallback.panel.sessionContext.kernelChanged.disconnect(
          kernelChangeCallback.callback
        );
      }
      kernelChangeCallback = {
        callback: createKernelChangeCallback(panel),
        panel
      };
      panel.sessionContext.kernelChanged.connect(kernelChangeCallback.callback);

      if (panel.sessionContext.session?.kernel?.id !== kernelId) {
        const kernelId = panel.sessionContext.session?.kernel?.id;
        if (kernelId) {
          setKernelId(kernelId);
          const path = panel.sessionContext.session?.model.path;
          setPath(path);
          requestUsage(kernelId).then(usage => setUsage(usage));
        }
      }
    };
    props.currentNotebookChanged.connect(notebookChangeCallback);
    return () => {
      props.currentNotebookChanged.disconnect(notebookChangeCallback);
      // In the ideal world we would disconnect kernelChangeCallback from
      // last panel here, but this can lead to a race condition. Instead,
      // we make sure there is ever only one callback active by holding
      // it in a global state.
    };
  }, [kernelId]);

  if (kernelId) {
    if (usage) {
      return !usage.hostname ? (
        <>
          <h3 className="jp-KernelUsage-section-separator">
            Kernel usage details are not available
          </h3>
          <div className="jp-KernelUsage-section-separator">
            Please check with your system administrator that you running
            IPyKernel version 6.10.0 or above.
          </div>
        </>
      ) : (
        <>
          <h3 className="jp-KernelUsage-section-separator">Kernel usage</h3>
          <div className="jp-KernelUsage-separator">
            Kernel Host: {usage.hostname}
          </div>
          <div className="jp-KernelUsage-separator">Notebook: {path}</div>
          <div className="jp-KernelUsage-separator">Kernel ID: {kernelId}</div>
          <div className="jp-KernelUsage-separator">
            Timestamp: {usage.timestamp?.toLocaleString()}
          </div>
          <div className="jp-KernelUsage-separator">
            Process ID: {usage.pid}
          </div>
          <div className="jp-KernelUsage-separator">
            CPU: {usage.kernel_cpu}% used
          </div>
          <div className="jp-KernelUsage-separator">
            Memory: {formatForDisplay(usage.kernel_memory)}
          </div>
          <hr className="jp-KernelUsage-section-separator"></hr>
          <h4 className="jp-KernelUsage-section-separator">Host CPU</h4>
          {usage.host_cpu_percent && (
            <div className="jp-KernelUsage-separator">
              {usage.host_cpu_percent.toFixed(1)}% used on {usage.cpu_count}{' '}
              CPUs
            </div>
          )}
          <h4 className="jp-KernelUsage-section-separator">
            Host Virtual Memory
          </h4>
          <div className="jp-KernelUsage-separator">
            Active: {formatForDisplay(usage.host_virtual_memory.active)}
          </div>
          <div className="jp-KernelUsage-separator">
            Available: {formatForDisplay(usage.host_virtual_memory.available)}
          </div>
          <div className="jp-KernelUsage-separator">
            Free: {formatForDisplay(usage.host_virtual_memory.free)}
          </div>
          <div className="jp-KernelUsage-separator">
            Inactive: {formatForDisplay(usage.host_virtual_memory.inactive)}
          </div>
          {usage.host_virtual_memory.percent && (
            <div className="jp-KernelUsage-separator">
              Percent used: {usage.host_virtual_memory.percent.toFixed(1)}%
            </div>
          )}
          <div className="jp-KernelUsage-separator">
            Total: {formatForDisplay(usage.host_virtual_memory.total)}
          </div>
          <div className="jp-KernelUsage-separator">
            Used: {formatForDisplay(usage.host_virtual_memory.used)}
          </div>
          <div className="jp-KernelUsage-separator">
            Wired: {formatForDisplay(usage.host_virtual_memory.wired)}
          </div>
        </>
      );
    }
  }
  return <h3>Kernel usage is not available</h3>;
};

export class KernelUsageWidget extends ReactWidget {
  private _widgetAdded: ISignal<INotebookTracker, NotebookPanel | null>;
  private _currentNotebookChanged: ISignal<
    INotebookTracker,
    NotebookPanel | null
  >;
  private _panel: KernelUsagePanel;
  constructor(props: {
    widgetAdded: ISignal<INotebookTracker, NotebookPanel | null>;
    currentNotebookChanged: ISignal<INotebookTracker, NotebookPanel | null>;
    panel: KernelUsagePanel;
  }) {
    super();
    this._widgetAdded = props.widgetAdded;
    this._currentNotebookChanged = props.currentNotebookChanged;
    this._panel = props.panel;
  }

  protected render(): React.ReactElement<any> {
    return (
      <KernelUsage
        widgetAdded={this._widgetAdded}
        currentNotebookChanged={this._currentNotebookChanged}
        panel={this._panel}
      />
    );
  }
}
