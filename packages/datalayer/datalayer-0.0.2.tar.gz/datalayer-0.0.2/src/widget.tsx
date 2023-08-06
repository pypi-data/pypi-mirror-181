import { ReactWidget } from '@jupyterlab/apputils';

import DemoComponent from './component/MockComponent';

export class CounterWidget extends ReactWidget {
  constructor() {
    super();
    this.addClass('dla-Container');
  }

  render(): JSX.Element {
    return <DemoComponent />;
  }
}
