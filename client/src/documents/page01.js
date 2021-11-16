//cafe
import React, { Component } from "react";

class Page01 extends React.Component{
    constructor(props) {
        super();

        this.state = {
            menu: 0,
        };
    }

    render(){

        return(
            <div className="docs">
                <h2>01. WCTT 설치</h2>
                <div className="doc-contents">
                    <ul>
                        <li>1. WCTT를 이용하기 위해서는 먼저 Node.js와 Python을 설치해야 합니다.</li>
                        <li>2. Git에 배포된 WCTT의 소스 파일을 내려받습니다.</li>
                            <li>3. 내려받은 WCTT의 소스 파일 중 [install.bat]을 [우클릭]으로 선택하여 나타나는 메뉴에서 [관리자 권한으로 실행]을 선택합니다.</li>
                        <li>- install.bat은 사용자의 PC에 사용자 인터페이스를 실행하기 위해 필요한 Node.js와 Python의 각종 패키지를 설치합니다.</li>
                        <li>- 또한, 패키지가 설치되는 경로를 시스템 환경 변수에 자동으로 등록해줍니다.</li>
                        <li>- WCTT 사용을 위해 설치되는 Node.js와 Python이 패키지 목록은 아래와 같습니다.</li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default Page01;