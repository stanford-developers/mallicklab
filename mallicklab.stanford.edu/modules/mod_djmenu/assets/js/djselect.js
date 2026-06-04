/**
 * @version $Id:$
 * @package DJ-Menu
 * @copyright Copyright (C) 2012 DJ-Extensions.com, All rights reserved.
 * @license DJ-Extensions.com Proprietary Use License
 * @author url: http://dj-extensions.com
 * @author email contact@dj-extensions.com
 * @developer Szymon Woronowski - szymon.woronowski@design-joomla.eu
 */
(function($){function addOptionsFromDJMenu(e,f,g){var h='';for(i=0;i<g;i++){h+='- '}e.each(function(a){var b=a.getElement('a');var c=a.getElement('ul');if(b){var d=new Element('option',{value:b.get('href'),text:h+b.get('text')}).inject(f);if(!b.get('href')){d.set('disabled',true)}if(a.hasClass('active')){f.set('value',d.get('value'))}}if(c)addOptionsFromDJMenu(c.getChildren('li'),f,g+1)})}window.addEvent('domready',function(){$$('.dj-main').each(function(a){var b=new Element('select',{id:a.get('id')+'select','class':'inputbox dj-select',events:{change:function(){if(this.get('value'))window.location=this.get('value')}}});var c=a.getChildren('li.dj-up');addOptionsFromDJMenu(c,b,0);b.inject(a,'after')})})})(document.id);