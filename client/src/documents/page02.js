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
                <h2>02. 수집 작업 등록 및 조작</h2>
                <div className="doc-contents">
                    <ul>
                        <li>WCTT가 정상적으로 실행되면 [그림1]과 같은 화면이 나타납니다.</li>
                        <li>수집 작업을 등록하기 위해서는 작업 이름과 키워드를 입력하고, 수집 기간과 수집하고자 하는 채널을 선택한 후 등록하기 버튼을 누르면 됩니다.</li>
                        <li>키워드를 여러 개 입력하기 위해서는 추가 버튼을 눌러 새로운 입력 칸을 생성하면 됩니다.</li>
                        <li>작업이 정상적으로 등록되면 [그림2]와 같이 DB에 작업이 추가되며, 곧 [그림3]처럼 추가된 작업이 목록에 나타나게 됩니다.</li>
                        <li>우측의 [시작하기] 버튼을 누르면 [그림4]와 같이 작업 진행상황이 갱신되며 수집 작업이 시작됩니다.</li>
                        <li>작업의 진행상황은 실시간으로 갱신되며, 수집 채널별 상세한 진행상황은 수집 작업을 눌러 [그림5]의 팝업창에서 확인할 수 있습니다.</li>
                        <li>수집 작업을 종료하고 싶다면, [정지하기] 버튼을 누르면 됩니다. </li>
                        <li>수집 작업을 삭제하고 싶다면, [삭제하기] 버튼을 누르면 됩니다. [삭제하기]는 반드시 수집 작업이 정지된 상태에서만 가능합니다.</li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default Page02;