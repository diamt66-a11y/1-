// ==========================================================================
// 솔로프레너 가이드 - 인터랙션 및 프리미엄 프론트엔드 제어 (app.js)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. 다크 모드 / 라이트 모드 테마 스위치
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  
  // 로컬 스토리지 또는 시스템 기본값에 따른 테마 세팅
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);
  updateThemeIcon(currentTheme);

  themeToggle.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    let nextTheme = theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    localStorage.setItem('theme', nextTheme);
    updateThemeIcon(nextTheme);
  });

  function updateThemeIcon(theme) {
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  // 2. 모바일 메뉴 반응형 토글
  const menuToggle = document.getElementById('menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', () => {
      navMenu.classList.toggle('mobile-active');
      if (navMenu.classList.contains('mobile-active')) {
        navMenu.style.display = 'flex';
        navMenu.style.flexDirection = 'column';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '100%';
        navMenu.style.left = '0';
        navMenu.style.width = '100%';
        navMenu.style.background = 'var(--glass-bg)';
        navMenu.style.backdropFilter = 'blur(20px)';
        navMenu.style.borderBottom = '1px solid var(--border-color)';
        navMenu.style.padding = '1.5rem';
        navMenu.style.gap = '1.2rem';
        navMenu.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
      } else {
        navMenu.removeAttribute('style');
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        navMenu.classList.remove('mobile-active');
        navMenu.removeAttribute('style');
      }
    });
  }

  // 3. 모달 (Modal) 관련 요소 제어
  const postModal = document.getElementById('post-modal');
  const modalClose = document.getElementById('modal-close');
  const modalCategory = document.getElementById('modal-category');
  const modalTitle = document.getElementById('modal-title');
  const modalDate = document.getElementById('modal-date');
  const modalAuthor = document.getElementById('modal-author');
  const modalBody = document.getElementById('modal-body');

  function openPostModal(post) {
    if (!postModal) return;
    
    modalCategory.textContent = normalizeCategory(post.category);
    modalTitle.textContent = post.title;
    modalDate.textContent = `발행일: ${post.date}`;
    modalAuthor.textContent = `작성자: ${normalizeAuthor(post.author)}`;
    
    // 본문 내용 채우기 (HTML 호환)
    modalBody.innerHTML = post.content || `<p>${post.excerpt}</p>`;
    
    // 애니메이션 활성화
    postModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closePostModal() {
    if (!postModal) return;
    postModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (modalClose) {
    modalClose.addEventListener('click', closePostModal);
  }

  // 모달 오버레이 영역 클릭 시 닫기
  if (postModal) {
    postModal.addEventListener('click', (e) => {
      if (e.target === postModal) {
        closePostModal();
      }
    });
  }

  // ESC 키 클릭 시 닫기
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closePostModal();
    }
  });

  // 4. 깨진 인코딩 복구 함수 (Fail-safe)
  function normalizeCategory(category) {
    if (!category) return '일반';
    const trimmed = category.trim();
    if (trimmed.includes('鍮꾩쫰') || trimmed.includes('비즈니스')) {
      return '비즈니스';
    }
    if (trimmed.includes('수익') || trimmed.includes('딆씪')) {
      return '수익화';
    }
    if (trimmed.includes('기획') || trimmed.includes('자동화')) {
      return '기획';
    }
    return trimmed;
  }

  function normalizeAuthor(author) {
    if (!author) return '솔로프레너';
    const trimmed = author.trim();
    if (trimmed.includes('넄濡') || trimmed.includes('솔로')) {
      return '솔로프레너';
    }
    return trimmed;
  }

  // 5. 데이터 패칭 & 빌드
  const postsGrid = document.querySelector('.posts-grid');
  const featuredPostArea = document.getElementById('featured-post-area');
  const recentPostsList = document.getElementById('recent-posts-list');
  const filterButtons = document.querySelectorAll('.filter-btn');
  const sidebarCatLinks = document.querySelectorAll('.sidebar-cat-link');
  
  let allPosts = [];
  
  if (postsGrid) {
    fetch('posts.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('포스트 데이터를 불러오는 데 실패했습니다.');
        }
        return response.json();
      })
      .then(posts => {
        // ID 순 또는 날짜 순 내림차순 정렬 (최신 글이 위로 오게)
        allPosts = posts.sort((a, b) => b.id - a.id);
        
        // 카테고리별 개수 세팅
        calculateCategoryCounts(allPosts);
        
        // 메인 영역 렌더링
        renderLayout(allPosts);
        
        // 이벤트 바인딩
        setupFilterEvents();
      })
      .catch(error => {
        console.error('Error loading posts:', error);
        postsGrid.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: 4rem; color: var(--text-secondary);">
            <p style="font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">⚠️ 블로그 포스트를 불러올 수 없습니다.</p>
            <small style="color: var(--accent-color);">서버 상태 또는 posts.json 파일을 확인해 주세요.</small>
          </div>
        `;
      });
  }

  // 카테고리 수량 집계 및 사이드바 바인딩
  function calculateCategoryCounts(posts) {
    const counts = {
      '비즈니스': 0,
      '수익화': 0,
      '기획': 0,
      '일반': 0
    };

    posts.forEach(post => {
      const normCat = normalizeCategory(post.category);
      if (counts[normCat] !== undefined) {
        counts[normCat]++;
      } else {
        counts['일반']++;
      }
    });

    Object.keys(counts).forEach(cat => {
      const badge = document.querySelector(`[data-cat-count="${cat}"]`);
      if (badge) {
        badge.textContent = counts[cat];
      }
    });
  }

  // 전체 레이아웃 스마트 빌더
  function renderLayout(posts) {
    if (!posts || posts.length === 0) {
      if (featuredPostArea) featuredPostArea.innerHTML = '';
      postsGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 4rem; color: var(--text-secondary);">
          <p style="font-size: 1.1rem; font-weight: 600;">등록된 글이 없습니다.</p>
        </div>
      `;
      return;
    }

    // 1. Featured Post (가장 최신 글 1개)
    const featuredPost = posts[0];
    renderFeaturedPost(featuredPost);

    // 2. 나머지 글들을 포스트 그리드에 배치 (Featured Post 제외)
    const remainingPosts = posts.slice(1);
    renderGridPosts(remainingPosts);

    // 3. 최근 글 3개 사이드바 렌더링
    renderRecentPostsWidget(posts.slice(0, 3));
  }

  // 히어로 피처드 포스트 렌더링
  function renderFeaturedPost(post) {
    if (!featuredPostArea) return;
    
    const bgStyle = post.themeColor ? `background-image: ${post.themeColor};` : 'background-image: linear-gradient(135deg, #ff4f00 0%, #ff8b3d 100%);';
    const normCategory = normalizeCategory(post.category);
    
    featuredPostArea.innerHTML = `
      <div class="featured-post">
        <div class="featured-img-wrap">
          <div class="featured-img" style="${bgStyle}"></div>
        </div>
        <div class="featured-content">
          <span class="featured-badge">FEATURED ARTICLE</span>
          <div class="featured-meta">
            <span>📅 ${post.date}</span>
            <span>✍️ ${normalizeAuthor(post.author)}</span>
          </div>
          <h2 class="featured-title">
            <a href="#" class="post-trigger" data-id="${post.id}">${post.title}</a>
          </h2>
          <p class="featured-excerpt">${post.excerpt}</p>
          <a href="#" class="read-more post-trigger" data-id="${post.id}">자세히 읽기 →</a>
        </div>
      </div>
    `;

    // 이벤트 추가
    featuredPostArea.querySelectorAll('.post-trigger').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openPostModal(post);
      });
    });
  }

  // 그리드 일반 카드 리스트 렌더링
  function renderGridPosts(posts) {
    postsGrid.innerHTML = '';
    
    if (posts.length === 0) {
      postsGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
          <p style="font-size: 1rem; font-weight: 500;">추가 등록된 다른 글이 없습니다.</p>
        </div>
      `;
      return;
    }

    posts.forEach(post => {
      const card = document.createElement('article');
      card.className = 'post-card';
      
      const bgStyle = post.themeColor ? `background-image: ${post.themeColor};` : 'background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);';
      const normCategory = normalizeCategory(post.category);

      card.innerHTML = `
        <div class="post-card-img-wrap">
          <div class="post-card-img" style="${bgStyle}"></div>
        </div>
        <div class="post-card-content">
          <span class="post-card-category">${normCategory}</span>
          <div class="post-card-meta">
            <span>${post.date}</span>
            <span>By ${normalizeAuthor(post.author)}</span>
          </div>
          <h3 class="post-card-title">
            <a href="#" class="post-trigger" data-id="${post.id}">${post.title}</a>
          </h3>
          <p class="post-card-excerpt">${post.excerpt}</p>
          <a href="#" class="read-more post-trigger" data-id="${post.id}">자세히 읽기 →</a>
        </div>
      `;
      
      // 이벤트 연결
      card.querySelectorAll('.post-trigger').forEach(el => {
        el.addEventListener('click', (e) => {
          e.preventDefault();
          openPostModal(post);
        });
      });

      postsGrid.appendChild(card);
    });
  }

  // 사이드바 최근 글 위젯 렌더링
  function renderRecentPostsWidget(posts) {
    if (!recentPostsList) return;
    recentPostsList.innerHTML = '';

    posts.forEach(post => {
      const item = document.createElement('div');
      item.className = 'recent-post-item';
      
      const bgStyle = post.themeColor ? `background-image: ${post.themeColor};` : 'background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);';

      item.innerHTML = `
        <div class="recent-post-thumb" style="${bgStyle}"></div>
        <div class="recent-post-details">
          <h4 class="recent-post-title">
            <a href="#" class="recent-trigger" data-id="${post.id}">${post.title}</a>
          </h4>
          <span class="recent-post-date">${post.date}</span>
        </div>
      `;

      item.querySelector('.recent-trigger').addEventListener('click', (e) => {
        e.preventDefault();
        openPostModal(post);
      });

      recentPostsList.appendChild(item);
    });
  }

  // 필터 클릭 이벤트 핸들러
  function setupFilterEvents() {
    // 1. 카테고리 네비게이션 필터 (전체보기, 비즈니스 등)
    filterButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        filterButtons.forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');

        const category = e.currentTarget.getAttribute('data-category');
        handleFilter(category);
      });
    });

    // 2. 사이드바 카테고리 클릭 연동
    sidebarCatLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const category = e.currentTarget.getAttribute('data-category');
        
        // 메인 필터 버튼 액티브 동기화
        filterButtons.forEach(b => {
          if (b.getAttribute('data-category') === category) {
            b.classList.add('active');
          } else {
            b.classList.remove('active');
          }
        });

        handleFilter(category);
        
        // 메인화면으로 스크롤 이동
        const mainElement = document.querySelector('main');
        if (mainElement) {
          mainElement.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // 필터 로직 분기
  function handleFilter(category) {
    if (category === 'all') {
      // 전체보기 시 기존 히어로 포스트 + 서브 그리드 복원
      if (featuredPostArea) featuredPostArea.style.display = 'grid';
      renderLayout(allPosts);
    } else {
      // 카테고리 개별 필터 적용 시, 히어로 포스트 영역을 숨기고 전체를 일반 카드로 리스트 출력
      if (featuredPostArea) featuredPostArea.style.display = 'none';
      const filtered = allPosts.filter(post => normalizeCategory(post.category) === category);
      renderGridPosts(filtered);
    }
  }
});
