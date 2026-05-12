import { StrictMode, Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

class ErrorBoundary extends Component<{children: ReactNode}, {hasError: boolean, error: Error | null, info: string}> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, error: null, info: "" };
  }
  static getDerivedStateFromError(error: Error) { 
    return { hasError: true, error, info: "" }; 
  }
  componentDidCatch(_error: Error, info: ErrorInfo) { 
    this.setState({ info: info.componentStack || "" });
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{color:'red', padding:'20px', backgroundColor: 'black', height: '100vh', overflow: 'auto'}}>
          <h2>Application Crashed!</h2>
          <pre style={{whiteSpace: 'pre-wrap'}}>{this.state.error?.toString()}</pre>
          <pre style={{whiteSpace: 'pre-wrap'}}>{this.state.info}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
