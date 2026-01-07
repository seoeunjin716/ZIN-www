import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: '파일이 없습니다.' },
        { status: 400 }
      );
    }

    // 파일을 버퍼로 변환
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // 저장 경로 설정
    // cv.seoeunjin.com/app/data/yolo 폴더
    // www.seoeunjin.com에서 cv.seoeunjin.com으로 가는 경로
    const baseDir = join(process.cwd(), '..', 'cv.seoeunjin.com', 'app', 'data', 'yolo');
    
    // 폴더가 없으면 생성
    await mkdir(baseDir, { recursive: true });

    // 파일명 생성 (원본 파일명 사용)
    const fileName = file.name;
    const filePath = join(baseDir, fileName);

    // 파일 저장
    await writeFile(filePath, buffer);

    return NextResponse.json({
      success: true,
      message: '파일이 성공적으로 저장되었습니다.',
      fileName: fileName,
      path: filePath,
    });
  } catch (error) {
    console.error('파일 저장 오류:', error);
    return NextResponse.json(
      { error: '파일 저장 중 오류가 발생했습니다.', details: String(error) },
      { status: 500 }
    );
  }
}

