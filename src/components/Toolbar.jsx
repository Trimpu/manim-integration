import React, { useRef } from 'react';

const Toolbar = ({ 
  onFileChange, 
  onZoomIn, 
  onZoomOut, 
  currentPage, 
  totalPages, 
  scale,
  backendStatus
}) => {
  const fileInputRef = useRef(null);

  const handleOpenClick = () => {
    fileInputRef.current?.click();
  };

  const formatScale = (scale) => {
    return Math.round(scale * 100);
  };

  const getBackendStatusIcon = () => {
    switch (backendStatus) {
      case 'ready': return '🟢';
      case 'offline': return '🔴';
      case 'error': return '🟡';
      case 'checking': return '⏳';
      default: return '❓';
    }
  };

  const getBackendStatusText = () => {
    switch (backendStatus) {
      case 'ready': return 'AI Ready';
      case 'offline': return 'Backend Offline';
      case 'error': return 'Config Error';
      case 'checking': return 'Checking...';
      default: return 'Unknown';
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between shadow-sm">
      <div className="flex items-center space-x-4">
        <button
          onClick={handleOpenClick}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
        >
          📁 Open PDF
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={onFileChange}
          className="hidden"
        />
      </div>

      <div className="flex items-center space-x-4">
        {totalPages > 0 && (
          <span className="text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
        )}
        
        {/* Backend Status Indicator */}
        <div className="flex items-center space-x-2">
          <span className="text-xs">{getBackendStatusIcon()}</span>
          <span className="text-xs text-gray-600">{getBackendStatusText()}</span>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={onZoomOut}
          disabled={scale <= 0.5}
          className="bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
          title="Zoom out"
        >
          🔍−
        </button>
        
        <span className="text-sm text-gray-600 min-w-[60px] text-center">
          {formatScale(scale)}%
        </span>
        
        <button
          onClick={onZoomIn}
          disabled={scale >= 3.0}
          className="bg-gray-100 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
          title="Zoom in"
        >
          🔍+
        </button>
      </div>
    </div>
  );
};

export default Toolbar;
