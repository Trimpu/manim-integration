import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';
import Toolbar from './Toolbar';
import FloatingButton from './FloatingButton';
import VideoPlayer from './VideoPlayer';
import ExplanationViewer from './ExplanationViewer';
import LoadingModal from './LoadingModal';
import { mathVideoAPI } from '../services/api';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

const PdfViewer = () => {
  const [numPages, setNumPages] = useState(null);
  const [scale, setScale] = useState(1.0);
  const [file, setFile] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const [selectionPosition, setSelectionPosition] = useState({ x: 0, y: 0 });
  const [showFloatingButton, setShowFloatingButton] = useState(false);
  
  // Video generation states
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [generationMessage, setGenerationMessage] = useState('');
  const [currentTaskId, setCurrentTaskId] = useState(null);
  
  // Video display states
  const [showVideoPlayer, setShowVideoPlayer] = useState(false);
  const [currentVideoUrl, setCurrentVideoUrl] = useState('');
  const [currentVideoTitle, setCurrentVideoTitle] = useState('');
  
  // Explanation display states
  const [showExplanationViewer, setShowExplanationViewer] = useState(false);
  const [currentExplanation, setCurrentExplanation] = useState('');
  const [currentExplanationTitle, setCurrentExplanationTitle] = useState('');
  
  // Backend status
  const [backendStatus, setBackendStatus] = useState('checking');
  
  const containerRef = useRef(null);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    }
  };

  const zoomIn = () => {
    setScale(prevScale => Math.min(prevScale + 0.2, 3.0));
  };

  const zoomOut = () => {
    setScale(prevScale => Math.max(prevScale - 0.2, 0.5));
  };

  const handleTextSelection = useCallback(() => {
    const selection = window.getSelection();
    let selectedText = selection.toString().trim();
    
    // Fix spacing issues in selected text from PDF
    if (selectedText) {
      // Remove strange characters that might come from PDF parsing
      selectedText = selectedText.replace(/[♠♣♥♦]/g, ' ');
      // Add spaces before capital letters that follow lowercase letters
      selectedText = selectedText.replace(/([a-z])([A-Z])/g, '$1 $2');
      // Add spaces before numbers when they follow letters
      selectedText = selectedText.replace(/([a-zA-Z])(\d)/g, '$1 $2');
      // Add spaces after numbers when they're followed by letters
      selectedText = selectedText.replace(/(\d)([a-zA-Z])/g, '$1 $2');
      // Fix common mathematical terms that get concatenated
      selectedText = selectedText.replace(/([a-z])(cm|mm|m|kg|g|°|π)/g, '$1 $2');
      selectedText = selectedText.replace(/(cm|mm|m|kg|g|°|π)([a-zA-Z])/g, '$1 $2');
      // Add space before "and", "of", "the", "is", "to", etc. when they're concatenated
      selectedText = selectedText.replace(/([a-z])(and|of|the|is|to|in|by|with|for)/g, '$1 $2');
      // Clean up multiple spaces and trim
      selectedText = selectedText.replace(/\s+/g, ' ').trim();
    }
    
    if (selectedText && selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      
      if (rect.width > 0 && rect.height > 0) {
        setSelectedText(selectedText);
        // Use viewport coordinates (fixed positioning)
        setSelectionPosition({
          x: rect.left + rect.width / 2,
          y: rect.top - 60 // Position above the selection
        });
        setShowFloatingButton(true);
      }
    } else {
      setShowFloatingButton(false);
      setSelectedText('');
    }
  }, []);

  useEffect(() => {
    let selectionTimeout;
    
    const handleSelectionChange = () => {
      // Clear previous timeout
      if (selectionTimeout) {
        clearTimeout(selectionTimeout);
      }
      
      // Debounce the selection handling
      selectionTimeout = setTimeout(() => {
        handleTextSelection();
      }, 100); // 100ms delay
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    
    // Also handle mouseup events on the PDF container for better responsiveness
    const handleMouseUp = () => {
      setTimeout(handleTextSelection, 50);
    };
    
    const container = containerRef.current;
    if (container) {
      container.addEventListener('mouseup', handleMouseUp);
    }
    
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      if (container) {
        container.removeEventListener('mouseup', handleMouseUp);
      }
      if (selectionTimeout) {
        clearTimeout(selectionTimeout);
      }
    };
  }, [handleTextSelection]);

  // Check backend status on component mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const status = await mathVideoAPI.checkSetup();
        setBackendStatus(status.status === 'ok' ? 'ready' : 'error');
        
        if (status.status !== 'ok') {
          console.warn('Backend setup issue:', status.message);
        }
      } catch (error) {
        setBackendStatus('offline');
        console.error('Backend is offline:', error);
      }
    };
    
    checkBackend();
  }, []);

  const handleVisualize = async (options = {}) => {
    if (!selectedText.trim()) return;
    
    console.log('Starting video generation for:', selectedText);
    
    try {
      setIsGenerating(true);
      setGenerationProgress(0);
      setGenerationMessage('Initializing video generation...');
      
      // Clear selection and hide floating button
      window.getSelection().removeAllRanges();
      setShowFloatingButton(false);
      
      // Start video generation
      const response = await mathVideoAPI.generateVideo(selectedText, options);
      setCurrentTaskId(response.task_id);
      
      // Poll for status updates
      pollGenerationStatus(response.task_id);
      
    } catch (error) {
      console.error('Error starting video generation:', error);
      setIsGenerating(false);
      setGenerationMessage('Failed to start video generation');
      
      // Show error notification
      alert('Failed to start video generation. Please make sure the backend is running.');
    }
  };

  const pollGenerationStatus = async (taskId) => {
    try {
      const status = await mathVideoAPI.checkStatus(taskId);
      
      setGenerationProgress(status.progress || 0);
      setGenerationMessage(status.message || 'Processing...');
      
      if (status.status === 'completed' && status.video_path) {
        // Generation completed successfully
        setIsGenerating(false);
        
        // Check if it's a video file or explanation file
        if (status.video_path.endsWith('.mp4')) {
          // It's a video file
          setCurrentVideoUrl(`http://localhost:5000/api/download/${encodeURIComponent(status.video_path)}`);
          setCurrentVideoTitle(selectedText.substring(0, 50) + (selectedText.length > 50 ? '...' : ''));
          setShowVideoPlayer(true);
        } else if (status.video_path.endsWith('.json')) {
          // It's an explanation file
          try {
            const response = await fetch(`http://localhost:5000/api/download/${encodeURIComponent(status.video_path)}`);
            const explanationData = await response.json();
            setCurrentExplanation(explanationData.explanation);
            setCurrentExplanationTitle(explanationData.topic);
            setShowExplanationViewer(true);
          } catch (error) {
            console.error('Error loading explanation:', error);
            alert('Error loading explanation');
          }
        }
        setSelectedText('');
        
      } else if (status.status === 'failed') {
        // Generation failed
        setIsGenerating(false);
        alert('Generation failed: ' + status.message);
        
      } else if (status.status === 'generating') {
        // Still generating, continue polling
        setTimeout(() => pollGenerationStatus(taskId), 2000);
        
      } else {
        // Unknown status or not found
        setIsGenerating(false);
        alert('Unknown error occurred during generation');
      }
      
    } catch (error) {
      console.error('Error checking generation status:', error);
      setIsGenerating(false);
      alert('Error checking generation status');
    }
  };

  const handleCancelGeneration = () => {
    setIsGenerating(false);
    setCurrentTaskId(null);
    setGenerationProgress(0);
    setGenerationMessage('');
  };

  const handleContainerClick = (e) => {
    // If clicking outside of selected text, clear selection
    if (showFloatingButton && !e.target.closest('button')) {
      setTimeout(() => {
        const selection = window.getSelection();
        if (!selection.toString().trim()) {
          setShowFloatingButton(false);
          setSelectedText('');
        }
      }, 10);
    }
  };

  const getCurrentPageNumber = () => {
    if (!containerRef.current || !numPages) return 1;
    
    const container = containerRef.current;
    const scrollTop = container.scrollTop;
    const containerHeight = container.clientHeight;
    
    // Estimate which page is currently visible based on scroll position
    const pageHeight = containerHeight / scale;
    const currentPage = Math.floor(scrollTop / pageHeight) + 1;
    
    return Math.min(Math.max(currentPage, 1), numPages);
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <Toolbar 
        onFileChange={handleFileChange}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        currentPage={getCurrentPageNumber()}
        totalPages={numPages || 0}
        scale={scale}
        backendStatus={backendStatus}
      />
      
      <div 
        ref={containerRef}
        className="flex-1 overflow-auto bg-gray-200 relative"
        style={{ scrollBehavior: 'smooth' }}
        onClick={handleContainerClick}
      >
        {file ? (
          <div className="flex flex-col items-center py-4">
            <Document
              file={file}
              onLoadSuccess={onDocumentLoadSuccess}
              className="max-w-full"
            >
              {Array.from(new Array(numPages), (el, index) => (
                <div key={`page_${index + 1}`} className="mb-4 shadow-lg">
                  <Page 
                    pageNumber={index + 1}
                    scale={scale}
                    className="border border-gray-300 bg-white"
                    renderTextLayer={true}
                    renderAnnotationLayer={true}
                  />
                </div>
              ))}
            </Document>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-500">
              <div className="text-6xl mb-4">📄</div>
              <p className="text-xl mb-2">No PDF selected</p>
              <p className="text-sm">Use the "Open PDF" button to load a document</p>
              
              {backendStatus === 'offline' && (
                <div className="mt-4 p-3 bg-red-100 border border-red-200 rounded-md max-w-md mx-auto">
                  <p className="text-sm text-red-800">
                    ⚠️ Backend is offline. Start the Flask server to enable video generation.
                  </p>
                </div>
              )}
              
              {backendStatus === 'error' && (
                <div className="mt-4 p-3 bg-yellow-100 border border-yellow-200 rounded-md max-w-md mx-auto">
                  <p className="text-sm text-yellow-800">
                    ⚠️ Backend configuration issue. Check your environment setup.
                  </p>
                </div>
              )}
              
              {backendStatus === 'ready' && (
                <div className="mt-4 p-3 bg-green-100 border border-green-200 rounded-md max-w-md mx-auto">
                  <p className="text-sm text-green-800">
                    ✅ AI video generation is ready!
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
        
        {showFloatingButton && (
          <FloatingButton
            onVisualize={handleVisualize}
            position={selectionPosition}
            selectedText={selectedText}
          />
        )}
      </div>
      
      {/* Loading Modal for Video Generation */}
      <LoadingModal
        isVisible={isGenerating}
        progress={generationProgress}
        message={generationMessage}
        onCancel={handleCancelGeneration}
      />
      
      {/* Video Player Modal */}
      {showVideoPlayer && (
        <VideoPlayer
          videoUrl={currentVideoUrl}
          title={currentVideoTitle}
          onClose={() => setShowVideoPlayer(false)}
        />
      )}
      
      {/* Explanation Viewer Modal */}
      {showExplanationViewer && (
        <ExplanationViewer
          explanation={currentExplanation}
          title={currentExplanationTitle}
          onClose={() => setShowExplanationViewer(false)}
        />
      )}
    </div>
  );
};

export default PdfViewer;
