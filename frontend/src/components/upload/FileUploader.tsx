import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, File, X, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface FileUploaderProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
  disabled?: boolean;
}

const FileUploader: React.FC<FileUploaderProps> = ({ 
  onFileSelect, 
  selectedFile, 
  disabled = false 
}) => {
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file && file.type === 'text/csv') {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    maxFiles: 1,
    disabled,
    onDragEnter: () => setDragActive(true),
    onDragLeave: () => setDragActive(false),
  });

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFileSelect(null);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Card className="w-full max-w-2xl mx-auto border-dashed border-2">
      <CardContent className="p-8">
        <div
          {...getRootProps()}
          className={cn(
            "relative cursor-pointer transition-all duration-200",
            isDragActive || dragActive ? "scale-105" : "",
            disabled ? "cursor-not-allowed opacity-50" : ""
          )}
        >
          <input {...getInputProps()} />
          
          {!selectedFile ? (
            <div className="text-center space-y-4">
              <div className={cn(
                "mx-auto w-16 h-16 rounded-full flex items-center justify-center transition-colors",
                isDragActive || dragActive 
                  ? "bg-primary text-primary-foreground" 
                  : "bg-muted text-muted-foreground"
              )}>
                <Upload className="h-8 w-8" />
              </div>
              
              <div className="space-y-2">
                <h3 className="text-lg font-semibold">
                  {isDragActive ? "Drop your CSV file here" : "Upload CSV File"}
                </h3>
                <p className="text-muted-foreground">
                  Drag and drop your CSV file here, or click to browse
                </p>
                <p className="text-sm text-muted-foreground">
                  Only CSV files are supported
                </p>
              </div>
              
              <Button variant="outline" type="button" disabled={disabled}>
                Browse Files
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <File className="h-6 w-6 text-primary" />
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-muted-foreground">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
              
              <div className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={removeFile}
                  disabled={disabled}
                  className="h-8 w-8 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FileUploader;