// Next.js 프로젝트의 components/FileUpload.tsx 로 복사하세요
'use client';

import { useState } from 'react';

interface UploadResult {
  success: boolean;
  filename: string;
  original_filename: string;
  path: string;
  size: number;
  size_mb: number;
}

interface FileInfo {
  filename: string;
  size: number;
  size_mb: number;
  created: string;
  modified: string;
}

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // XMLHttpRequest로 진행률 추적
      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percent = (e.loaded / e.total) * 100;
          setProgress(Math.round(percent));
        }
      });

      const uploadPromise = new Promise<UploadResult>((resolve, reject) => {
        xhr.addEventListener('load', () => {
          if (xhr.status === 200) {
            resolve(JSON.parse(xhr.responseText));
          } else {
            reject(new Error(`업로드 실패: ${xhr.statusText}`));
          }
        });

        xhr.addEventListener('error', () => {
          reject(new Error('네트워크 오류'));
        });

        xhr.open('POST', `${API_URL}/api/upload`);
        xhr.send(formData);
      });

      const data = await uploadPromise;
      setResult(data);
      setFile(null);
      
      // 파일 목록 새로고침
      await fetchFiles();
      
      // 파일 input 초기화
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
    } catch (err: any) {
      console.error('업로드 실패:', err);
      setError(err.message || '파일 업로드 실패');
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  const fetchFiles = async () => {
    try {
      const response = await fetch(`${API_URL}/api/files`);
      const data = await response.json();
      if (data.success) {
        setFiles(data.files);
      }
    } catch (err) {
      console.error('파일 목록 조회 실패:', err);
    }
  };

  const deleteFile = async (filename: string) => {
    if (!confirm(`'${filename}' 파일을 삭제하시겠습니까?`)) return;

    try {
      const response = await fetch(`${API_URL}/api/files/${filename}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      
      if (data.success) {
        alert('파일이 삭제되었습니다');
        await fetchFiles();
      }
    } catch (err) {
      console.error('파일 삭제 실패:', err);
      alert('파일 삭제 실패');
    }
  };

  // 컴포넌트 마운트 시 파일 목록 로드
  useState(() => {
    fetchFiles();
  });

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6">파일 업로드</h2>
      
      {/* 업로드 섹션 */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              파일 선택
            </label>
            <input
              id="file-input"
              type="file"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100
                cursor-pointer"
            />
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                선택된 파일: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </p>
            )}
          </div>
          
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg
              hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed
              transition-colors font-semibold"
          >
            {uploading ? `업로드 중... ${progress}%` : '업로드'}
          </button>

          {uploading && (
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-500 h-2.5 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {result && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-2">✓ 업로드 완료</h3>
              <div className="text-sm text-green-700 space-y-1">
                <p>파일명: {result.filename}</p>
                <p>원본: {result.original_filename}</p>
                <p>크기: {result.size_mb} MB</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 파일 목록 섹션 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold">업로드된 파일 ({files.length})</h3>
          <button
            onClick={fetchFiles}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
          >
            새로고침
          </button>
        </div>
        
        {files.length === 0 ? (
          <p className="text-gray-500 text-center py-8">업로드된 파일이 없습니다</p>
        ) : (
          <div className="space-y-2">
            {files.map((file) => (
              <div
                key={file.filename}
                className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{file.filename}</p>
                  <p className="text-sm text-gray-500">
                    {file.size_mb} MB · {new Date(file.created).toLocaleString('ko-KR')}
                  </p>
                </div>
                <div className="flex gap-2">
                  <a
                    href={`${API_URL}/uploads/${file.filename}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
                  >
                    다운로드
                  </a>
                  <button
                    onClick={() => deleteFile(file.filename)}
                    className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    삭제
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

