"""
OWASP Maryam!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class main:

	def __init__(self, q, limit=15):
		""" piratebay search engine
			q         : query for search
			limit     : maximum result count
		"""
		self.framework = main.framework
		self.q = self.framework.urlib(q).quote_plus
		self.max = limit
		self._json = ''
		self._links_with_data = []

	def run_crawl(self):
		url = 'https://apibay.org/q.php'
		payload = {'q' : self.q, 'cat':''}
		self.framework.verbose('[PIRATEBAY] Searching piratebay...')
		try:
			req = self.framework.request(
					url=url,
					params=payload,
					allow_redirects=True)
		except:
			self.framework.error('ConnectionError.', 'util/piratebay', 'run_crawl')
			self.framework.error('Piratebay is missed!', 'util/piratebay', 'run_crawl')

		else:
			self._rawhtml = req.text
			self._json = req.json()

	def make_magnet(self, info_hash, name):
		return (f"magnet:?xt=urn:btih:{info_hash}&dn={name}"
			'&tr=udp://tracker.coppersurfer.tk:6969/announce'
			'&tr=udp://open.demonii.com:1337'
			'&tr=udp://tracker.openbittorrent.com:6969/announce'
			'&tr=udp://tracker.opentrackr.org:1337'
			'&tr=udp://tracker.leechers-paradise.org:6969/announce'
			'&tr=udp://tracker.dler.org:6969/announce'
			'&tr=udp://opentracker.i2p.rocks:6969/announce'
			'&tr=udp://47.ip-51-68-199.eu:6969/announce')

	@property
	def raw(self):
		return self._rawhtml

	@property
	def json(self):
		return self._json

	@property
	def links_with_data(self):
		for count,torrent in enumerate(self.json):
			if count == self.max:
				break

			title = torrent['name']
			info = torrent['info_hash']

			self._links_with_data.append({
				'title': title,
				'uploader': torrent['username'],
				'magnet': self.make_magnet(info, title),
				'seeders': torrent['seeders'],
				'leechers': torrent['leechers']
				})

		return self._links_with_data
