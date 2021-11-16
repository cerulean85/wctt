//cafe
import React, { Component } from "react";

class Page02 extends React.Component{
    constructor(props) {
        super();

        this.state = {
            menu: 0,
        };
    }

    render(){

        return(
            <div className="docs">
                <h2>03. 수집 데이터 확인</h2>
                <div className="doc-contents">
                    <ul>
                        <li>수집된 데이터는 사용자 PC의 [내 문서]의 [data]라는 경로에 저장됩니다. (Windows 10 기준)</li>
                        <li>사용자의 PC에 저장되는 데이터로는 html 파일, 본문 원본, 단어-빈도표, 동시 출현 행렬입니다.</li>
                        <li>모든 수집이 완료되면 html 파일과 같은 불필요한 데이터는 제거해주세요.</li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default Page02;