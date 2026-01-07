'use client';

import { useState, useCallback, useRef } from 'react';

interface FileItem {
    id: string;
    file: File;
    preview: string;
}

export default function PortfolioPage() {
    const [isDragging, setIsDragging] = useState(false);
    const [files, setFiles] = useState<FileItem[]>([]);
    const [saving, setSaving] = useState<string | null>(null); // 저장 중인 파일 ID
    const fileInputRef = useRef<HTMLInputElement>(null);

    // 파일을 FileItem으로 변환
    const processFiles = useCallback((fileList: FileList) => {
        const newFiles: FileItem[] = [];

        Array.from(fileList).forEach((file) => {
            // 이미지 파일만 허용
            if (file.type.startsWith('image/')) {
                const id = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
                const preview = URL.createObjectURL(file);
                newFiles.push({ id, file, preview });
            }
        });

        setFiles((prev) => [...prev, ...newFiles]);
    }, []);

    // 드래그 시작
    const handleDragEnter = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    }, []);

    // 드래그 중
    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    }, []);

    // 드래그 나감
    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    // 파일 정보를 포맷팅하는 함수
    const formatFileInfo = useCallback((file: File): string => {
        const size = file.size < 1024
            ? `${file.size} B`
            : file.size < 1024 * 1024
                ? `${(file.size / 1024).toFixed(1)} KB`
                : `${(file.size / 1024 / 1024).toFixed(2)} MB`;

        const type = file.type.split('/')[1]?.toUpperCase() || 'IMAGE';
        const lastModified = new Date(file.lastModified).toLocaleString('ko-KR');

        return `파일명: ${file.name}\n크기: ${size}\n타입: ${type}\n수정일: ${lastModified}`;
    }, []);

    // 드롭
    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            e.stopPropagation();
            setIsDragging(false);

            const droppedFiles = e.dataTransfer.files;
            if (droppedFiles.length > 0) {
                // 이미지 파일만 필터링
                const imageFiles = Array.from(droppedFiles).filter(file => file.type.startsWith('image/'));

                if (imageFiles.length === 0) {
                    alert('이미지 파일만 업로드 가능합니다.');
                    return;
                }

                // 각 파일의 정보를 alert로 표시
                if (imageFiles.length === 1) {
                    // 단일 파일인 경우
                    alert(`📁 파일 정보\n\n${formatFileInfo(imageFiles[0])}`);
                } else {
                    // 여러 파일인 경우
                    const fileInfoList = imageFiles.map((file, index) =>
                        `[${index + 1}] ${file.name} (${file.size < 1024 * 1024 ? `${(file.size / 1024).toFixed(1)} KB` : `${(file.size / 1024 / 1024).toFixed(2)} MB`})`
                    ).join('\n');

                    alert(`📁 업로드된 파일 (${imageFiles.length}개)\n\n${fileInfoList}`);
                }

                processFiles(droppedFiles);
            }
        },
        [processFiles, formatFileInfo]
    );

    // 파일 선택 (클릭)
    const handleFileChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            const selectedFiles = e.target.files;
            if (selectedFiles && selectedFiles.length > 0) {
                // 이미지 파일만 필터링
                const imageFiles = Array.from(selectedFiles).filter(file => file.type.startsWith('image/'));

                if (imageFiles.length === 0) {
                    alert('이미지 파일만 업로드 가능합니다.');
                    return;
                }

                // 각 파일의 정보를 alert로 표시
                if (imageFiles.length === 1) {
                    // 단일 파일인 경우
                    alert(`📁 파일 정보\n\n${formatFileInfo(imageFiles[0])}`);
                } else {
                    // 여러 파일인 경우
                    const fileInfoList = imageFiles.map((file, index) =>
                        `[${index + 1}] ${file.name} (${file.size < 1024 * 1024 ? `${(file.size / 1024).toFixed(1)} KB` : `${(file.size / 1024 / 1024).toFixed(2)} MB`})`
                    ).join('\n');

                    alert(`📁 업로드된 파일 (${imageFiles.length}개)\n\n${fileInfoList}`);
                }

                processFiles(selectedFiles);
            }
        },
        [processFiles, formatFileInfo]
    );

    // 파일 삭제
    const handleRemoveFile = useCallback((id: string) => {
        setFiles((prev) => {
            const fileToRemove = prev.find((f) => f.id === id);
            if (fileToRemove) {
                URL.revokeObjectURL(fileToRemove.preview);
            }
            return prev.filter((f) => f.id !== id);
        });
    }, []);

    // 드롭 영역 클릭
    const handleDropZoneClick = useCallback(() => {
        fileInputRef.current?.click();
    }, []);

    // 포트폴리오에 추가 (파일 저장)
    const handleSaveToPortfolio = useCallback(async (fileItem: FileItem) => {
        setSaving(fileItem.id);

        try {
            const formData = new FormData();
            formData.append('file', fileItem.file);

            const response = await fetch('/api/portfolio/save', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                alert(`✅ 포트폴리오에 추가되었습니다!\n\n파일명: ${result.fileName}`);
            } else {
                alert(`❌ 저장 실패: ${result.error || '알 수 없는 오류'}`);
            }
        } catch (error) {
            console.error('파일 저장 오류:', error);
            alert(`❌ 파일 저장 중 오류가 발생했습니다: ${error}`);
        } finally {
            setSaving(null);
        }
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
            <div className="mx-auto max-w-6xl">
                <h1 className="mb-8 text-4xl font-bold text-gray-900">포트폴리오</h1>

                {/* 드래그 앤 드롭 영역 */}
                <div
                    onClick={handleDropZoneClick}
                    onDragEnter={handleDragEnter}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    className={`
            relative mb-8 cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all
            ${isDragging
                            ? 'border-blue-500 bg-blue-50 scale-105'
                            : 'border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50'
                        }
          `}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        multiple
                        onChange={handleFileChange}
                        className="hidden"
                    />

                    <div className="flex flex-col items-center gap-4">
                        <div
                            className={`
                rounded-full p-4 transition-colors
                ${isDragging ? 'bg-blue-100' : 'bg-gray-100'}
              `}
                        >
                            <svg
                                className={`h-12 w-12 ${isDragging ? 'text-blue-600' : 'text-gray-600'}`}
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                                />
                            </svg>
                        </div>

                        <div>
                            <p className="text-xl font-semibold text-gray-700">
                                {isDragging ? '여기에 파일을 놓으세요' : '파일을 드래그하거나 클릭하여 업로드'}
                            </p>
                            <p className="mt-2 text-sm text-gray-500">
                                이미지 파일만 업로드 가능합니다
                            </p>
                        </div>
                    </div>
                </div>

                {/* 업로드된 파일 목록 - 작은 썸네일로 표시 */}
                {files.length > 0 && (
                    <div className="mb-8">
                        <h2 className="mb-4 text-2xl font-semibold text-gray-900">
                            업로드된 파일 ({files.length})
                        </h2>
                        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                            {files.map((fileItem) => (
                                <div
                                    key={fileItem.id}
                                    className="group relative overflow-hidden rounded-lg bg-white shadow-sm transition-all hover:shadow-md border border-gray-200"
                                >
                                    {/* 작은 썸네일 이미지 */}
                                    <div className="relative aspect-square w-full">
                                        <img
                                            src={fileItem.preview}
                                            alt={fileItem.file.name}
                                            className="h-full w-full object-cover"
                                        />
                                        {/* 삭제 버튼 - 항상 표시 */}
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleRemoveFile(fileItem.id);
                                            }}
                                            className="absolute top-1 right-1 rounded-full bg-red-500 p-1.5 opacity-0 transition-opacity group-hover:opacity-100 hover:bg-red-600"
                                            title="삭제"
                                        >
                                            <svg
                                                className="h-3 w-3 text-white"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    strokeWidth={2}
                                                    d="M6 18L18 6M6 6l12 12"
                                                />
                                            </svg>
                                        </button>
                                    </div>

                                    {/* 파일 정보 - 이미지 하단에 항상 표시 */}
                                    <div className="p-2">
                                        <p className="truncate text-xs font-medium text-gray-700 mb-1" title={fileItem.file.name}>
                                            {fileItem.file.name}
                                        </p>
                                        <p className="text-xs text-gray-500">
                                            {fileItem.file.size < 1024
                                                ? `${fileItem.file.size} B`
                                                : fileItem.file.size < 1024 * 1024
                                                    ? `${(fileItem.file.size / 1024).toFixed(1)} KB`
                                                    : `${(fileItem.file.size / 1024 / 1024).toFixed(2)} MB`}
                                        </p>
                                        <p className="text-xs text-gray-400 mt-0.5 mb-2">
                                            {fileItem.file.type.split('/')[1]?.toUpperCase() || 'IMAGE'}
                                        </p>
                                        {/* 포트폴리오에 추가 버튼 */}
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleSaveToPortfolio(fileItem);
                                            }}
                                            disabled={saving === fileItem.id}
                                            className="w-full rounded bg-blue-500 px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                                        >
                                            {saving === fileItem.id ? '저장 중...' : '포트폴리오에 추가'}
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* 파일 목록이 없을 때 */}
                {files.length === 0 && (
                    <div className="rounded-lg bg-white p-12 text-center">
                        <p className="text-gray-500">아직 업로드된 파일이 없습니다.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

