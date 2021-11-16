//cafe
import React, { Component } from "react";

class About extends React.Component{
    constructor(props) {
        super();

        this.state = {
            menu: 0,
        };
    }

    render(){
        return(
            <div>

                <div style={{
                    marginTop: 40,
                    marginLeft: 30,
                    marginRight: 0,
                    marginBottom: 40,
                    color: "#1F1F1F",
                    textAlign: "left",
                    borderBottom: '1px solid #000000',
                }}>
                    <h2>About WCTT</h2>
                    <hr width={"100%"} color={"#555555"}/>
                    <ul style={{lineHeight: 1.8, fontSize: 16, marginRight:30}}>
                        <li>WCTT는 Web Crawling system based on Tag path and Text appearance frequency의 약자입니다.</li>
                        <li>WCTT는 태그 경로 및 텍스트 출현 빈도 기반의 웹 크롤링 시스템입니다.</li>
                        <li>WCTT는 데스크톱 PC에서 이용할 수 있는 개인용 웹 크롤링 시스템입니다.</li>
                        <li>WCTT는 쉽고 편리한 텍스트 수집 환경을 제공합니다.</li>
                        <br/>
                        <li>CSS 선택자와 같이 태그/스타일 속성을 이용하여 웹 페이지에서 본문을 수집하는 기존의 웹 크롤러는 웹 페이지에서 본문을 수집하기 위해 수집 채널마다 다른 수집 로직을 구현해야 합니다.</li>
                        <li>따라서 기존의 웹 크롤러의 경우 웹 페이지 구조가 변경된다면 수집 로직을 수정해야 하고, 새로운 웹 사이트에서 본문을 수집하고자 한다면 새로운 수집 로직을 추가로 구현해야 합니다.</li>
                        <li>하지만 이러한 방법은 유지 관리와 수집 채널의 확장이 어려워 수집의 효율성을 저하시키는 요인으로 작용합니다.</li>
                        <li>예를 들어, 기존의 웹 크롤러의 경우에는 새로운 수집 채널을 추가하고 싶다면 해당 수집 채널에 맞는 수집 로직을 새롭게 구현할 것입니다.</li>
                        <li>이러한 문제점을 해결하기 위해서는 본문 수집 로직과 웹 페이지 사이의 의존성을 줄여야 하며, 이를 위해 웹 크롤러는 웹 페이지 구조가 달라도 동일한 수집 로직으로 본문을 수집할 수 있어야 합니다.</li>
                        <br/>
                        <li>WCTT는 지도학습 기반의 머신러닝으로 학습된 학습 모델을 이용하여 웹 페이지에서 본문을 수집합니다.</li>
                        <li>따라서 WCTT는 모든 수집 채널에 대해 동일한 수집 로직을 이용할 뿐만 아니라, 웹 페이지가 변경되거나 새로운 수집 채널을 추가하기 위해 수집 로직의 수정이나 구현이 필요없습니다.</li>
                        <li>즉, WCTT 사용자는 별도의 구현 과정없이 웹상의 텍스트를 수집할 수 있습니다.</li>
                        <li>학습 모델은 태그 경로 및 텍스트 출현 빈도 분석 기반의 방법으로 학습되었으며, 자세한 내용은 다음의 <a href={"https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE10608043"}>논문</a>을 참고해주세요.</li>
                        <br/>

                        <li>WCTT는 네이버 블로그, 인스타그램, 트위터, 동아일보, 중앙일보의 수집 채널을 지원하고 있습니다. (2021.11.14 기준)</li>
                    </ul>
                    <br/>
                    <br/>
                </div>
                <div style={{
                    marginTop: 40,
                    marginLeft: 0,
                    marginRight: 30,
                    marginBottom: 40,
                    height: 278,
                    borderBottom: '1px solid #000000',
                    color: "#1F1F1F"}}>
                    <h2 style={{paddingTop:20, textAlign:"right"}}>About Developer</h2>
                    <hr width={"100%"} color={"#555555"}/>
                    <img src="zhkim_profile.jpg" style={{width:"15%", height:200, float:"right"}}/>
                    <ul style={{lineHeight: 1.8, fontSize: 16, direction: "rtl", float:"right"}}>
                        <li>이름: 김 진환(Kim Jin-hwan)</li>
                        <li>한국기술교육대학교 컴퓨터공학과 석사</li>
                        <li>관심분야: 빅데이터 처리와 분석, 머신러닝</li>
                        <li>누구나 쉽게 빅데이터를 수집하고 분석할 수 있는 세상을 만들어 갑니다</li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default About;