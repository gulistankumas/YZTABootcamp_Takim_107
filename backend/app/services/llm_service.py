from typing import Dict, List, Optional, Any
import asyncio
import logging
import google.generativeai as genai
from app.core.config import settings
from app.services.reference_range_service import reference_range_service

logger = logging.getLogger(__name__)

class MedicalLLMService:
    """Tıbbi analiz için LLM servisi (Sadece Gemini)"""
    def __init__(self):
        self.gemini_model = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("✅ Gemini client başlatıldı")

    async def analyze_blood_test(self, test_results: List[Dict], patient_info: Dict) -> Dict:
        try:
            evaluated_results = []
            for test in test_results:
                evaluation = reference_range_service.evaluate_test_result(
                    test_name=test['test_name'],
                    value=test['value'],
                    age=patient_info['age'],
                    gender=patient_info.get('gender')
                )
                evaluated_results.append({
                    **test,
                    'evaluation': evaluation
                })
            prompt = self._create_blood_test_prompt(evaluated_results, patient_info)
            if self.gemini_model:
                response = await self._call_gemini(prompt)
            else:
                raise Exception("Gemini LLM client bulunamadı")
            llm_analysis = self._parse_analysis_response(response)
            return {
                'test_evaluations': evaluated_results,
                'llm_analysis': llm_analysis,
                'summary': self._create_summary(evaluated_results, llm_analysis)
            }
        except Exception as e:
            logger.error(f"LLM analiz hatası: {e}")
            return self._get_fallback_response()

    async def assess_health_risks(self, test_results: List[Dict], patient_info: Dict) -> Dict:
        try:
            evaluated_results = []
            for test in test_results:
                evaluation = reference_range_service.evaluate_test_result(
                    test_name=test['test_name'],
                    value=test['value'],
                    age=patient_info['age'],
                    gender=patient_info.get('gender')
                )
                evaluated_results.append({
                    **test,
                    'evaluation': evaluation
                })
            prompt = self._create_risk_assessment_prompt(evaluated_results, patient_info)
            if self.gemini_model:
                response = await self._call_gemini(prompt)
            else:
                raise Exception("Gemini LLM client bulunamadı")
            llm_analysis = self._parse_analysis_response(response)
            return llm_analysis
        except Exception as e:
            logger.error(f"LLM risk analiz hatası: {e}")
            return self._get_fallback_risk_response()

    async def generate_doctor_insights(self, test_results: List[Dict], symptoms: List[str], patient_info: Dict) -> Dict:
        try:
            evaluated_results = []
            for test in test_results:
                evaluation = reference_range_service.evaluate_test_result(
                    test_name=test['test_name'],
                    value=test['value'],
                    age=patient_info['age'],
                    gender=patient_info.get('gender')
                )
                evaluated_results.append({
                    **test,
                    'evaluation': evaluation
                })
            prompt = self._create_doctor_insights_prompt(evaluated_results, symptoms, patient_info)
            if self.gemini_model:
                response = await self._call_gemini(prompt)
            else:
                raise Exception("Gemini LLM client bulunamadı")
            llm_analysis = self._parse_analysis_response(response)
            return llm_analysis
        except Exception as e:
            logger.error(f"LLM doktor içgörü hatası: {e}")
            return self._get_fallback_doctor_response()

    async def generate_patient_education(self, diagnosis: str, treatment_plan: Dict, patient_language: str = "tr") -> Dict:
        try:
            prompt = self._create_patient_education_prompt(diagnosis, treatment_plan, patient_language)
            if self.gemini_model:
                response = await self._call_gemini(prompt)
            else:
                raise Exception("Gemini LLM client bulunamadı")
            llm_analysis = self._parse_analysis_response(response)
            return llm_analysis
        except Exception as e:
            logger.error(f"LLM hasta bilgilendirme hatası: {e}")
            return self._get_fallback_education_response()

    def _create_blood_test_prompt(self, evaluated_results: List[Dict], patient_info: Dict) -> str:
        """Kan tahlili analizi için prompt oluşturur"""
        prompt = f"""
        Sen deneyimli bir tıbbi analiz uzmanısın. Aşağıdaki kan tahlili sonuçlarını analiz et ve JSON formatında yanıt ver.

        Hasta Bilgileri:
        - Yaş: {patient_info.get('age', 'Bilinmiyor')}
        - Cinsiyet: {patient_info.get('gender', 'Bilinmiyor')}
        - Test Türü: {patient_info.get('test_type', 'Genel')}

        Test Sonuçları:
        {self._format_test_results(evaluated_results)}

        Lütfen aşağıdaki JSON formatında yanıt ver:

        {{
            "genel_değerlendirme": {{
                "genel_durum": "normal|dikkat|ciddi",
                "acil_durum": true/false,
                "genel_aciklama": "Genel durum açıklaması",
                "onemli_not": "Bu bir yapay zeka önerisidir, kesin tanı için klinik değerlendirme gerekir"
            }},
            "anormal_degerler": [
                {{
                    "test_adi": "Test adı",
                    "deger": "Test değeri",
                    "normal_aralik": "Normal aralık",
                    "durum": "normal|düşük|yüksek|kritik_düşük|kritik_yüksek",
                    "aciklama": "Tıbbi açıklama"
                }}
            ],
            "olası_hastalıklar": [
                "Olası hastalık 1",
                "Olası hastalık 2"
            ],
            "oneriler": {{
                "doktor_onerileri": [
                    "Doktor önerisi 1",
                    "Doktor önerisi 2"
                ],
                "yasam_tarzi": [
                    "Yaşam tarzı önerisi 1",
                    "Yaşam tarzı önerisi 2"
                ],
                "beslenme": [
                    "Beslenme önerisi 1",
                    "Beslenme önerisi 2"
                ],
                "uzmanlik_alani": [
                    "Uzmanlık alanı 1",
                    "Uzmanlık alanı 2"
                ],
                "takip_onerisi": "Takip önerisi"
            }},
            "hasta_mesaji": "Hastaya yönelik açıklama"
        }}

        Önemli Notlar:
        1. Sadece JSON formatında yanıt ver
        2. Hastayı korkutmayan, profesyonel bir dil kullan
        3. Tıbbi terminolojiyi doğru kullan
        4. Acil durumları net bir şekilde belirt
        5. Doktor dilinde, ancak anlaşılır açıklamalar yap
        """
        return prompt

    def _create_risk_assessment_prompt(self, evaluated_results: List[Dict], patient_info: Dict) -> str:
        """Risk değerlendirmesi için prompt oluşturur"""
        prompt = f"""
        Sen deneyimli bir tıbbi risk değerlendirme uzmanısın. Aşağıdaki test sonuçlarına göre sağlık risklerini değerlendir.

        Hasta Bilgileri:
        - Yaş: {patient_info.get('age', 'Bilinmiyor')}
        - Cinsiyet: {patient_info.get('gender', 'Bilinmiyor')}

        Test Sonuçları:
        {self._format_test_results(evaluated_results)}

        Lütfen aşağıdaki JSON formatında yanıt ver:

        {{
            "genel_risk_değerlendirmesi": {{
                "genel_durum": "normal|düşük_risk|orta_risk|yüksek_risk",
                "acil_durum": true/false,
                "genel_aciklama": "Risk değerlendirmesi açıklaması",
                "onemli_not": "Bu bir yapay zeka önerisidir, kesin değerlendirme için doktorunuza başvurun"
            }},
            "acil_riskler": [
                "Acil risk 1",
                "Acil risk 2"
            ],
            "kronik_riskler": [
                "Kronik risk 1",
                "Kronik risk 2"
            ],
            "30_gunluk_tahmin": {{
                "olası_komplikasyonlar": [
                    "Komplikasyon 1",
                    "Komplikasyon 2"
                ],
                "onleyici_tedbirler": [
                    "Önleyici tedbir 1",
                    "Önleyici tedbir 2"
                ],
                "takip_onerisi": "Takip önerisi"
            }},
            "genel_risk_puani": 0-100,
            "hasta_mesaji": "Hastaya yönelik risk açıklaması"
        }}

        Önemli Notlar:
        1. Sadece JSON formatında yanıt ver
        2. Risk seviyelerini objektif değerlendir
        3. Acil durumları net belirt
        4. Hastayı korkutmayan profesyonel dil kullan
        """
        return prompt

    def _create_doctor_insights_prompt(self, evaluated_results: List[Dict], symptoms: List[str], patient_info: Dict) -> str:
        """Doktor içgörüleri için prompt oluşturur"""
        prompt = f"""
        Sen deneyimli bir klinik uzmanısın. Aşağıdaki test sonuçları ve semptomları değerlendirerek doktorlar için klinik içgörüler sağla.

        Hasta Bilgileri:
        - Yaş: {patient_info.get('age', 'Bilinmiyor')}
        - Cinsiyet: {patient_info.get('gender', 'Bilinmiyor')}

        Test Sonuçları:
        {self._format_test_results(evaluated_results)}

        Semptomlar:
        {', '.join(symptoms) if symptoms else 'Belirtilmemiş'}

        Lütfen aşağıdaki JSON formatında yanıt ver:

        {{
            "genel_klinik_değerlendirme": {{
                "genel_durum": "normal|dikkat|ciddi",
                "acil_durum": true/false,
                "klinik_aciklama": "Klinik değerlendirme açıklaması",
                "onemli_not": "Bu bir yapay zeka önerisidir, klinik değerlendirme gerekir"
            }},
            "differential_diagnosis": [
                "Diferansiyel tanı 1",
                "Diferansiyel tanı 2"
            ],
            "ek_testler": [
                "Ek test 1",
                "Ek test 2"
            ]
        }}

        Önemli Notlar:
        1. Sadece JSON formatında yanıt ver
        2. Klinik terminolojiyi doğru kullan
        3. Diferansiyel tanıları önem sırasına göre sırala
        4. Doktor dilinde profesyonel açıklamalar yap
        """
        return prompt

    def _create_patient_education_prompt(self, diagnosis: str, treatment_plan: Dict, patient_language: str = "tr") -> str:
        """Hasta eğitimi için prompt oluşturur"""
        prompt = f"""
        Sen deneyimli bir hasta eğitimi uzmanısın. Aşağıdaki tanı ve tedavi planına göre hasta eğitim materyali hazırla.

        Tanı: {diagnosis}
        Tedavi Planı: {treatment_plan}

        Lütfen {patient_language} dilinde, aşağıdaki JSON formatında yanıt ver:

        {{
            "aciklama": "Hastalık/tanı açıklaması",
            "onemli_bulgular": "Önemli bulgular",
            "oneriler": "Genel öneriler"
        }}

        Önemli Notlar:
        1. Sadece JSON formatında yanıt ver
        2. {patient_language} dilinde yaz
        3. Hasta anlayacağı seviyede açıkla
        4. Profesyonel ama samimi olmayan bir dil kullan
        5. "Merhaba", "endişelenmeyin" gibi samimi ifadeler kullanma
        """
        return prompt

    def _format_test_results(self, evaluated_results: List[Dict]) -> str:
        """Test sonuçlarını formatlar"""
        formatted = []
        for result in evaluated_results:
            evaluation = result.get('evaluation', {})
            formatted.append(
                f"- {result['test_name']}: {result['value']} {result.get('unit', '')} "
                f"(Normal: {evaluation.get('reference_range', 'Bilinmiyor')}, "
                f"Durum: {evaluation.get('status', 'Bilinmiyor')})"
            )
        return '\n'.join(formatted)
    
    async def _call_gemini(self, prompt: str) -> str:
        """Google Gemini API çağrısı"""
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.LLM_TEMPERATURE,
                    max_output_tokens=4000,
                    top_p=0.8,
                    top_k=40
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API hatası: {e}")
            raise
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """LLM yanıtını parse eder"""
        try:
            import json
            return json.loads(response)
        except Exception:
            logger.error(f"JSON parse hatası: {response}")
            return self._get_fallback_response()
    
    def _create_summary(self, evaluated_results: List[Dict], llm_analysis: Dict) -> Dict:
        """Test sonuçları ve LLM analizini özetler"""
        # Anormal değerleri say
        abnormal_count = sum(1 for result in evaluated_results 
                           if result['evaluation']['status'] != 'normal')
        
        # Kritik değerleri say
        critical_count = sum(1 for result in evaluated_results 
                           if result['evaluation']['status'] in ['critical_low', 'critical_high'])
        
        # En yüksek risk seviyesini bul
        max_risk = max((result['evaluation']['risk_level'] for result in evaluated_results), 
                      key=lambda x: ['normal', 'low', 'high', 'critical'].index(x))
        
        return {
            'total_tests': len(evaluated_results),
            'abnormal_tests': abnormal_count,
            'critical_tests': critical_count,
            'max_risk_level': max_risk,
            'overall_status': llm_analysis.get('genel_değerlendirme', {}).get('genel_risk', 'unknown')
        }
    
    def _get_fallback_response(self) -> Dict:
        """Fallback yanıt"""
        return {
            'genel_değerlendirme': {
                'genel_durum': 'normal',
                'acil_durum': False,
                'genel_aciklama': 'Analiz sırasında teknik bir hata oluştu. Endişelenmeyin, bu normal bir durumdur.',
                'onemli_not': 'Bu bir yapay zeka önerisidir, kesin tanı için doktorunuza başvurun'
            },
            'anormal_degerler': [],
            'olası_hastalıklar': [],
            'oneriler': {
                'doktor_onerileri': ['Doktorunuzla görüşün'],
                'yasam_tarzi': ['Sağlıklı yaşam tarzını sürdürün'],
                'beslenme': ['Dengeli beslenmeye devam edin'],
                'uzmanlik_alani': [],
                'takip_onerisi': 'Doktorunuzla görüşün'
            },
            'hasta_mesaji': 'Analiz sırasında teknik bir hata oluştu. Bu durum endişe verici değildir. Doktorunuzla görüşerek gerekli bilgileri alabilirsiniz.'
        }
    
    def _get_fallback_risk_response(self) -> Dict:
        """Fallback risk yanıtı"""
        return {
            'genel_risk_değerlendirmesi': {
                'genel_durum': 'normal',
                'acil_durum': False,
                'genel_aciklama': 'Risk değerlendirmesi sırasında teknik bir hata oluştu. Endişelenmeyin.',
                'onemli_not': 'Bu bir yapay zeka önerisidir, kesin değerlendirme için doktorunuza başvurun'
            },
            'acil_riskler': [],
            'kronik_riskler': [],
            '30_gunluk_tahmin': {
                'olası_komplikasyonlar': [],
                'onleyici_tedbirler': [],
                'takip_onerisi': 'Doktorunuzla görüşün'
            },
            'genel_risk_puani': 0,
            'hasta_mesaji': 'Risk değerlendirmesi sırasında teknik bir hata oluştu. Bu durum endişe verici değildir. Doktorunuzla görüşerek gerekli bilgileri alabilirsiniz.'
        }
    
    def _get_fallback_doctor_response(self) -> Dict:
        """Fallback doktor yanıtı"""
        return {
            'genel_klinik_değerlendirme': {
                'genel_durum': 'normal',
                'acil_durum': False,
                'klinik_aciklama': 'Klinik değerlendirme sırasında teknik bir hata oluştu.',
                'onemli_not': 'Bu bir yapay zeka önerisidir, klinik değerlendirme gerekir'
            },
            'differential_diagnosis': [],
            'ek_testler': [],
        }

    def _get_fallback_education_response(self) -> Dict:
        """Fallback eğitim yanıtı"""
        return {
            'aciklama': 'Hasta bilgilendirme sırasında teknik bir hata oluştu.',
            'onemli_bulgular': '',
            'oneriler': ''
        }

llm_service = MedicalLLMService() 